from django.db import models


class state_tax_levy_config(models.Model):
    state = models.CharField(max_length=255, unique=True)
    deduction_basis = models.CharField(max_length=255, blank=True, null=True)
    withholding_limit = models.CharField(max_length=255, blank=True, null=True)
    withholding_limit_rule = models.CharField(
        max_length=455, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['state'])
        ]
        db_table = "state_tax_levy_config"


class state_tax_levy_exempt_amt_config(models.Model):
    # state_config = models.ForeignKey(
    #     state_tax_levy_config,
    #     on_delete=models.CASCADE,
    #     related_name="state_tax_levy_exempt_amounts"
    # )
    state = models.CharField(max_length=255,)
    pay_period = models.CharField(max_length=255)
    minimum_hourly_wage_basis = models.CharField(max_length=255)
    minimum_wage_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    multiplier_lt = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    condition_expression_lt = models.CharField(max_length=255,null=True, blank=True)
    lower_threshold_amount = models.DecimalField(
        max_digits=10, decimal_places=4)
    multiplier_ut = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    condition_expression_ut = models.CharField(max_length=255,null=True, blank=True)
    upper_threshold_amount = models.DecimalField(
        max_digits=10, decimal_places=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['state']),
            models.Index(fields=['pay_period', 'state']),
        ]
        db_table = "state_tax_levy_exempt_amt_config"


class state_tax_levy_applied_rule(models.Model):
    ee_id = models.CharField(max_length=1000, blank=True, null=True)
    case_id = models.CharField(max_length=1000, blank=True, null=True)
    state = models.CharField(max_length=1000, blank=True, null=True)
    pay_period = models.CharField(max_length=1000)
    deduction_basis = models.CharField(max_length=1000, blank=True, null=True)
    withholding_cap = models.CharField(max_length=1000, blank=True, null=True)
    withholding_limit = models.CharField(
        max_length=1000, blank=True, null=True)
    withholding_basis = models.CharField(
        max_length=1000, blank=True, null=True)
    withholding_limit_rule = models.CharField(
        max_length=1000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['case_id']),
            models.Index(fields=['ee_id'])
        ]
        db_table = "state_tax_levy_applied_rule"

class state_tax_levy_rule_edit_permission(models.Model):
    state = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    deduction_basis = models.CharField(max_length=255, blank=True, null=True)
    withholding_limit = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['state'])
        ]
        db_table = "state_tax_levy_rule_edit_permission"