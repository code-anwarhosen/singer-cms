import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cms.models import Account, Payment, Product, PRODUCT_CATEGORIES, Customer, Contract

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



@login_required
def product_list(request):
    categories = [cat[0] for cat in PRODUCT_CATEGORIES]
    products = Product.objects.all()

    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'cms/product_list.html', context)

@login_required
def create_product(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
    try:
        data = json.loads(request.body)
        
        required_fields = ['category', 'model']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({'status': 'error', 'message': f'"{field}" is required.'}, status=400)

        category = data['category']
        model = data['model']

        if not category or not model:
            return JsonResponse({'status': 'error', 'message': 'Product category or model can\'t be empty'})
        
        if Product.objects.filter(model=model).exists():
            return JsonResponse({'status': 'error', 'message': f'A product with this ({model}) model already exists!'})

        Product.objects.create(category=category, model=model)
        
        data = {
            'category': category,
            'model': model
        }
        return JsonResponse({'status': 'success', 'message': 'successfully added product model!', 'data': data})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'{e}'}, status=500)








# ----------- Create Account -------------#
@login_required
def create_account(request):
    user = request.user
    
    # if this condition true, return the template
    if request.method == 'GET':
        return render(request, 'cms/acc_creation_form.html')

    # if post request then, procced to create account
    try:
        data = json.loads(request.body)
        
        # Validate required fields
        required_fields = ['accountNumber', 'customerUid', 'selectedModel', 'cashValue', 
            'hireValue', 'downPayment', 'monthlyPayment', 'length', 'saleDate'
        ]
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({'status': 'error', 'message': f'"{field}" is required.'}, status=400)

        account_number = data['accountNumber']
        customer_uid = data['customerUid']
        selected_model = data['selectedModel']

        # Check if account already exists
        if Account.objects.filter(acc_num=account_number.upper()).exists():
            return JsonResponse({'status': 'error', 'message': f'An account already exists with this "{account_number}" account number.'}, status=400)

        # Check for customer
        customer = Customer.objects.filter(pk=customer_uid).first()
        if not customer:
            return JsonResponse({'status': 'error', 'message': f'Customer with UID {customer_uid} does not exist.'}, status=404)

        # Check for product
        product = Product.objects.filter(model=selected_model).first()
        if not product:
            return JsonResponse({'status': 'error', 'message': 'There is no product associated with the selected model.'}, status=400)

        # Create account
        account = Account.objects.create(
            created_by=user, acc_num=account_number, date=data['saleDate'], 
            customer=customer, product=product, status='active'
        )

        # Create contract
        try:
            contract = Contract.objects.create(
                account=account,
                cash_price=int(data['cashValue']),
                hire_price=int(data['hireValue']),
                down_payment=int(data['downPayment']),
                monthly_payment=int(data['monthlyPayment']),
                tenure=int(data['length'])
            )
        except Exception as e:
            return JsonResponse({'status': 'success', 'message': 'Account created successfully, but there might be issues with the contract information.'})

        return JsonResponse({
            'status': 'success', 
            'message': 'Account created successfully!', 
            'data': {'accountNumber': account.acc_num
        }})

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'{e}'}, status=500)


@login_required
def pre_creation_data(request):
    user = request.user

    if request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    
    try:
        customers = user.customers.all()
        serialized_customers = [
            {
                'uid': customer.pk,
                'name': customer.name,
                'phone': customer.phone,
                'address': customer.address,
            }
            for customer in customers
        ]

        categories = [
            {'value': category[0], 'name': category[1]}
            for category in PRODUCT_CATEGORIES
        ]

        products = Product.objects.all()
        serialized_products = [
            {
                'category': product.category,
                'model': product.model
            }
            for product in products
        ]

        data = {
            'customers': serialized_customers,
            'productCategories': categories,
            'products': serialized_products,
        }
        return JsonResponse({'success': True, 'data': data})

    except Exception as e:
        return JsonResponse({'success': False, 'message': 'An error occurred while fetching data.'}, status=500)


@login_required
def create_customer(request):
    user = request.user

    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    try:
        # Parse JSON data
        data = json.loads(request.body)

        # Extract fields
        name = data.get('fullname')
        phone = data.get('phone')
        address = data.get('address')

        # Validate required fields
        if not name or not phone or not address:
            return JsonResponse({'status': 'error', 'message': 'Full Name, Phone, and Address are required fields.'}, status=400)

        # Check if customer already exists with the given phone number
        customer = Customer.objects.filter(phone=phone).first()
        if customer:
            response_data = {
                'uid': customer.pk, 'name': customer.name,
                'phone': customer.phone, 'address': customer.address,
            }
            return JsonResponse({'status': 'success',
                'message': f'Customer already exists with this phone number. UID: {customer.pk}',
                'customer': response_data}, status=200)


        # Create new customer
        customer = Customer.objects.create(
            created_by=user, name=name,
            phone=phone, address=address,
        )

        # Prepare response data
        response_data = {
            'uid': customer.pk, 'name': customer.name,
            'phone': customer.phone, 'address': customer.address,
        }

        return JsonResponse({'status': 'success', 'message': 'Customer created successfully!',
            'customer': response_data}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data.'}, status=400)

    except ValueError as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': 'An error occurred while creating the customer.'}, status=500)

