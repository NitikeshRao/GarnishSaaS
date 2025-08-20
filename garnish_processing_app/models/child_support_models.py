from django.db import models


class disposable_earning_rules(models.Model):
    state = models.CharField(max_length=255)
    disposable_earnings = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "disposable_earning_rules"



class WithholdingRules(models.Model):
    state = models.ForeignKey('garnish_processing_app.State', on_delete=models.CASCADE)
    rule = models.CharField(max_length=255)
    allocation_method = models.CharField(max_length=255)
    withholding_limit = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "withholding_rules"
        
class WithholdingLimit(models.Model):
    rule = models.ForeignKey(WithholdingRules, on_delete=models.CASCADE, related_name='limits')
    wl = models.CharField(max_length=10)  
    supports_2nd_family = models.CharField(max_length=10, null=True, blank=True)  
    arrears_of_more_than_12_weeks = models.CharField(max_length=10, null=True, blank=True) 
    number_of_orders = models.CharField(max_length=10, null=True, blank=True)  
    weekly_de_code = models.CharField(max_length=10, null=True, blank=True)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "withholding_limit"
