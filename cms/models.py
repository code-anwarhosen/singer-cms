from django.db import models
from datetime import date
from django.core.validators import RegexValidator
from user.models import User
import re

class Customer(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customers')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, help_text="Enter 11 digit phone number")
    address = models.CharField(max_length=500, blank=True, null=True)
    
    class Meta:
        ordering = ['-id']
        
    def save(self, *args, **kwargs):
        """
        Accept only 01712345678  or
        01912-345678 format phone number
        """
        if not re.match(r"^01[3-9][\d]{2}-?[\d]{6}$", self.phone):
            raise ValueError("Invalid phone number format")
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.name


PRODUCT_CATEGORIES = (
    ('REF', 'Refrigerator'),
    ('FREEZER', 'Deep Freezer'),
    ('TV', 'Television'),
    ('AC', 'Air Conditioner'),
    ('WM', 'Washing Machine'),
    ('OVEN', 'Microwave Oven'),
    ('SM', 'Sewing Machine'),
    ('COM', 'Computer'),
    ('OTHER', 'Others'),
)
class Product(models.Model):
    model = models.CharField(max_length=50, unique=True, primary_key=True)
    category = models.CharField(max_length=50, choices=PRODUCT_CATEGORIES, default=PRODUCT_CATEGORIES[0][0])

    class Meta:
        ordering = ['category', 'model']
        
    def save(self, *args, **kwargs):
        self.model = self.model.upper()
        
        if not re.match(r"^[A-Z]{4,6}-[A-Z\d-/.]{4,30}$", self.model):
            raise ValueError("Not a valid product model.")
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.category} : {self.model}'


class Account(models.Model):
    ACC_STATUSES = (
        ('planned', 'Planned'),
        ('active', 'Active'),
        ('closed', 'Closed'),
    )
    acc_num = models.CharField(max_length=10, primary_key=True, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, blank=True, null=True, related_name='accounts')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)

    status = models.CharField(max_length=20, choices=ACC_STATUSES, default=ACC_STATUSES[0][0], 
        db_index=True  # <--- faster queries like Account.objects.filter(status="active")
    )
    date = models.DateField(default=date.today, 
        db_index=True # <--- faster queries like Account.objects.filter(date__year=2025)
    )
    remarks = models.CharField(max_length=255, blank=True, null=True)
    
    class Meta:
        ordering = ['-acc_num']
        
    def save(self, *args, **kwargs):
        pattern = re.compile(r"^[a-zA-Z]{3}-[hH][0-9]+$")
        if not pattern.match(self.acc_num):
            raise ValueError("Invalid Account Number Format")
        
        self.acc_num = self.acc_num.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.acc_num


class Contract(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE, related_name='contract')
    
    cash_price = models.PositiveIntegerField(default=0, blank=True)
    hire_price = models.PositiveIntegerField(default=0, blank=True)

    down_payment = models.PositiveIntegerField()
    total_paid = models.PositiveIntegerField(default=0, editable=False)
    
    monthly_payment = models.PositiveIntegerField(blank=True, null=True)
    tenure = models.PositiveIntegerField(default=12)

    @property
    def cash_bal(self):
        if self.cash_price is not None:
            return self.cash_price - self.total_paid
        return None
    
    @property
    def hire_bal(self):
        if self.hire_price is not None:
            return self.hire_price - self.total_paid
        return None


    class Meta:
        ordering = ['-id']
        
    def __str__(self):
        if self.account:
            return self.account.acc_num
        return f'contract id - {id}'


class Payment(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='payments')
    
    amount = models.PositiveIntegerField()
    receipt_id = models.CharField(max_length=50, unique=True)
    date = models.DateField(default=date.today)

    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        if self.contract and self.contract.account:
            return self.contract.account.acc_num
        return f"{self.receipt_id} : {self.amount}"
