from django.db import models
from garnish_processing_app.models.shared_models import PayPeriod, State, ExemptConfig, ThresholdAmount



class garnishment_fees(models.Model):
    state = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    pay_period = models.CharField(max_length=255)
    amount = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=255)
    rules = models.CharField(max_length=255)
    payable_by = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['state']),
            models.Index(fields=['type']),
            models.Index(fields=['pay_period', 'state']),
        ]
        db_table = "garnishment_fees"


class garnishment_fees_rules(models.Model):
    rule = models.CharField(max_length=255)
    maximum_fee_deduction = models.CharField(max_length=255)
    per_pay_period = models.DecimalField(max_digits=10, decimal_places=2)
    per_month = models.DecimalField(max_digits=10, decimal_places=2)
    per_remittance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['rule'])
        ]
        db_table = "garnishment_fees_rules"

class garnishment_fees_states_rule(models.Model):
    state = models.CharField(max_length=255)
    pay_period = models.CharField(max_length=255)
    rule = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['state'])
        ]
        db_table = "garnishment_fees_states_rule"
