from django.db import models


class IRSPublication1494(models.Model):
    year =  models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        db_table = "irs_publication_1494"
        # unique_together = ('year',)

    def __str__(self):
        return str(self.year)

class FedFilingStatus(models.Model):
    fs_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True) 
    default_exempt_amt = models.FloatField(help_text="Default exempt amount for older/blind")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "fed_filing_status"

    def __str__(self):
        return self.name


class StdExemptions(models.Model):
    std_id = models.AutoField(primary_key=True)
    year = models.ForeignKey(IRSPublication1494, on_delete=models.CASCADE)
    fs = models.ForeignKey(FedFilingStatus, on_delete=models.CASCADE)
    pp = models.ForeignKey('garnish_processing_app.PayPeriod', on_delete=models.CASCADE)
    num_exemptions = models.CharField(max_length=100, null=True, blank=True)
    exempt_amt = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "std_exemptions"
        unique_together = ('year', 'fs', 'pp','num_exemptions')


class AddExemptions(models.Model):
    add_id = models.AutoField(primary_key=True)
    year = models.ForeignKey(IRSPublication1494, on_delete=models.CASCADE)
    fs = models.ForeignKey(FedFilingStatus, on_delete=models.CASCADE)
    num_exemptions = models.PositiveIntegerField()
    daily = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    weekly = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    biweekly = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    semimonthly = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    monthly = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "add_exemptions"
        unique_together = ('year', 'fs', 'num_exemptions')
        