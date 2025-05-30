from django.contrib import admin
from cms.models import Customer, Product, Payment, Account, Contract

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Payment)
admin.site.register(Account)

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ['account', 'cash_price', 'hire_price', 'down_payment', 'cash_bal', 'hire_bal']