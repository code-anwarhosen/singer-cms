from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'cms/home.html')

@login_required
def get_accounts(request):
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
