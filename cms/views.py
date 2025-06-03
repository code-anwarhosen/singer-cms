import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cms.models import Account, Payment

@login_required
def home(request):
    return render(request, 'cms/home.html')

@login_required
def get_accounts(request):
    '''
    js fetch:
    Fetch all accounts of logged in user
        called from home page to populate 
        customer list in home page
    '''
    user = request.user

    accounts = user.accounts.all()
    if not accounts:
        return JsonResponse({'success': False})
    
    serialized_data = [{
        'pk': acc.pk,
        'name': acc.customer.name if acc.customer else "Unknown",
        'phone': acc.customer.phone if acc.customer else "N/A",
        'account': acc.acc_num,
        'balance': acc.contract.cash_bal if acc.contract else 0,
        'avatar': '/static/images/user.png',
        'status': acc.status,
    } for acc in accounts]
    return JsonResponse({'success': True, 'accounts': serialized_data})

@login_required
def get_account_details(request, pk):
    account = Account.objects.filter(pk=pk).first()

    if not account:
        messages.info(request, 'The account you are trying to access does not exists!')
        return redirect('home')
    
    payments = account.contract.payments.all().order_by('date') if account.contract else None
    return render(request, 'cms/account_details.html', {'account': account, 'payments': payments})


@login_required
def create_payment(request, pk):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
    account = Account.objects.filter(pk=pk).first()
    contract = account.contract
    
    if not contract:
        return JsonResponse({'status': 'error', 'message': 'The account you\'re trying to make payment is invalid!'})
    
    try:
        data = json.loads(request.body)
        
        required_fields = ['paymentAmount', 'receiptNumber', 'paymentDate']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({'status': 'error', 'message': f'"{field}" is required.'}, status=400)

        paymentAmount = data['paymentAmount']
        receiptNumber = data['receiptNumber']
        paymentDate = data['paymentDate']
        
        try:
            paymentAmount = int(paymentAmount)
        except Exception:
            return JsonResponse({'status': 'error', 'message': 'Invalid amount.'})

        if paymentAmount > contract.hire_bal:
            return JsonResponse({'status': 'error', 'message': 'Payment amount exceeds hire balance.'})
        
        if Payment.objects.filter(receipt_id=receiptNumber).exists():
            return JsonResponse({'status': 'error', 'message': f'"{receiptNumber}" this receipt ID already exists.'})

        payment = Payment.objects.create(
            contract=contract,
            date=paymentDate,
            receipt_id=receiptNumber,
            amount=int(paymentAmount)
        )

        data = {
            'paymentDate': payment.date,
            'receiptId': payment.receipt_id,
            'paymentAmount': payment.amount,
            'cashBalance': contract.cash_bal
        }
        return JsonResponse({'status': 'success', 'message': 'Payment created!', 'data': data})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'{e}'}, status=500)

