from django.db import models

class payroll(models.Model):
    cid = models.CharField(max_length=255)
    eeid = models.CharField(max_length=255)
    payroll_date = models.DateField()
    pay_date = models.DateField()
    gross_pay = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    net_pay = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    tax_federal_income_tax = models.DecimalField(
        max_digits=13, decimal_places=2)
    tax_state_tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    tax_local_tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    tax_medicare_tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    tax_social_security = models.CharField(max_length=255)
    deduction_sdi = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    deduction_medical_insurance = models.DecimalField(
        max_digits=13, decimal_places=2)
    deduction_401k = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    deduction_union_dues = models.DecimalField(
        max_digits=13, decimal_places=2)
    deduction_voluntary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    type = models.CharField(max_length=255)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['cid']),
            models.Index(fields=['eeid']),
            models.Index(fields=['cid', 'eeid']),
        ]
        db_table = "payroll"


class payroll_taxes_batch_data(models.Model):
    # employee_case = models.OneToOneField(
    #     employee_batch_data,
    #     to_field='case_id',
    #     on_delete=models.CASCADE,
    #     related_name='payroll_data'
    # )
    ee_id = models.CharField(max_length=255, unique=True)
    case_id = models.CharField(max_length=255, unique=True)
    wages = models.DecimalField(max_digits=10, decimal_places=2)
    commission_and_bonus = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    non_accountable_allowances = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    gross_pay = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    debt = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    exemption_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    net_pay = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    federal_income_tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    social_security_tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    medicare_tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    state_tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    local_tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    union_dues = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    wilmington_tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    medical_insurance_pretax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    industrial_insurance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    life_insurance = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    california_sdi = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['case_id']),
            models.Index(fields=['ee_id', 'case_id']),
        ]

        db_table = "payroll_taxes_batch_data"