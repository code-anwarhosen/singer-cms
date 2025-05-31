from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import models
from cms.models import Contract, Payment

def recalculate_total_paid(contract):
    payments_total = contract.payments.aggregate(total=models.Sum('amount'))['total'] or 0
    contract.total_paid = (contract.down_payment or 0) + payments_total
    contract.save(update_fields=['total_paid'])


@receiver(post_save, sender=Payment)
def update_contract_total_on_payment_save(sender, instance, created, **kwargs):
    recalculate_total_paid(instance.contract)


@receiver(post_delete, sender=Payment)
def update_contract_total_on_payment_delete(sender, instance, **kwargs):
    recalculate_total_paid(instance.contract)


@receiver(post_save, sender=Contract)
def update_total_paid_on_contract_save(sender, instance, created, **kwargs):
    recalculate_total_paid(instance)
