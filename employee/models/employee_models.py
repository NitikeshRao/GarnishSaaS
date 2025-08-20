from django.db import models

class employee_detail(models.Model):
    ee_id = models.CharField(max_length=255)
    case_id = models.CharField(max_length=255)
    age = models.CharField(max_length=255)
    social_security_number = models.CharField(max_length=255)
    is_blind = models.BooleanField(null=True, blank=True)
    home_state = models.CharField(max_length=255)
    work_state = models.CharField(max_length=255)
    gender = models.CharField(max_length=255, null=True, blank=True)
    number_of_exemptions = models.IntegerField()
    filing_status = models.CharField(max_length=255)
    marital_status = models.CharField(max_length=255)
    number_of_student_default_loan = models.IntegerField()
    support_second_family = models.BooleanField()
    spouse_age = models.IntegerField(null=True, blank=True)
    is_spouse_blind = models.BooleanField(null=True, blank=True)
    record_import = models.DateTimeField(auto_now_add=True)
    record_updated = models.DateTimeField(auto_now_add=True)
    garnishment_fees_status = models.BooleanField()
    garnishment_fees_suspended_till = models.DateField()
    pay_period = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['ee_id']),
            models.Index(fields=['case_id']),
            models.Index(fields=['ee_id', 'case_id']),
        ]
        db_table = "employee_detail"


class employee_batch_data(models.Model):
    ee_id = models.CharField(max_length=255, unique=True)
    case_id = models.CharField(max_length=255, unique=True)
    work_state = models.CharField(max_length=255)
    no_of_exemption_including_self = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    pay_period = models.CharField(max_length=255, null=True, blank=True)
    filing_status = models.CharField(max_length=255, null=True, blank=True)
    age = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    is_blind = models.BooleanField(null=True, blank=True)
    is_spouse_blind = models.BooleanField(null=True, blank=True)
    spouse_age = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    support_second_family = models.CharField(max_length=255,null=True, blank=True)
    no_of_student_default_loan = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    arrears_greater_than_12_weeks = models.CharField(max_length=255,null=True, blank=True)
    no_of_dependent_exemption = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['case_id']),
            models.Index(fields=['ee_id', 'case_id']),
        ]

        db_table = "employee_batch_data"

    def __str__(self):
        return f"Employee {self.ee_id} - Case {self.case_id}"

