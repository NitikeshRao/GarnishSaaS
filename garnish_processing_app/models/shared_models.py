from django.db import models


class PayPeriod(models.Model):
    pp_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table ="payperiod"

        
class State(models.Model):
    state_code = models.CharField(max_length=100,unique=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table="state_data"

class ExemptConfig(models.Model):
    state = models.ForeignKey('State', on_delete=models.CASCADE)
    pay_period = models.ForeignKey('PayPeriod', on_delete=models.CASCADE)
    debt_type = models.CharField(max_length=100,null=True, blank=True)
    is_filing_status = models.BooleanField(default=False)
    wage_basis = models.CharField(max_length=100,null=True, blank=True)
    wage_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    percent_limit = models.IntegerField(null=True, blank=True)
    start_gt_5dec24 = models.BooleanField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table ="exempt_config"
        
class ThresholdAmount(models.Model):
    config = models.ForeignKey(ExemptConfig, on_delete=models.CASCADE)
    lower_threshold_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    lower_threshold_percent1 = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    lower_threshold_percent2 = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    mid_threshold_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    mid_threshold_percent = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    upper_threshold_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    upper_threshold_percent = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    de_range_lower_to_upper_threshold_percent = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    de_range_lower_to_mid_threshold_percent = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    de_range_mid_to_upper_threshold_percent =models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    exempt_amt = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    filing_status_percent =models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table ="threshold_amount"



class ThresholdCondition(models.Model):
    threshold = models.ForeignKey(ThresholdAmount, on_delete=models.CASCADE)
    multiplier_lt = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    condition_expression_lt = models.CharField(max_length=100, null=True, blank=True)
    multiplier_mid = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    condition_expression_mid = models.CharField(max_length=100, null=True, blank=True)
    multiplier_ut = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    condition_expression_ut = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table ="threshold_condition"



class GarnishmentType(models.Model):
    type = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type

    class Meta:
        db_table = "garnishment_type"


class PriorityOrders(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    garnishment_type = models.ForeignKey(GarnishmentType, on_delete=models.CASCADE)
    priority_order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "priority_order"
        # unique_together = ('priority_order', 'garnishment_type')