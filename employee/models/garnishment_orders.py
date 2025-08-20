from django.db import models


class withholding_order_data(models.Model):
    date = models.CharField(max_length=250)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    case_id = models.CharField(max_length=255)
    order_id = models.CharField(max_length=255)
    remittance_id = models.CharField(max_length=255)
    fein = models.CharField(max_length=255)
    employee_name = models.CharField(max_length=255)

    child1_name = models.CharField(max_length=255, blank=True, null=True)
    child2_name = models.CharField(max_length=255, blank=True, null=True)
    child3_name = models.CharField(max_length=255, blank=True, null=True)
    child4_name = models.CharField(max_length=255, blank=True, null=True)
    child5_name = models.CharField(max_length=255, blank=True, null=True)
    child6_name = models.CharField(max_length=255, blank=True, null=True)

    child1_dob = models.CharField(max_length=255, blank=True, null=True)
    child2_dob = models.CharField(max_length=255, blank=True, null=True)
    child3_dob = models.CharField(max_length=255, blank=True, null=True)
    child4_dob = models.CharField(max_length=255, blank=True, null=True)
    child5_dob = models.CharField(max_length=255, blank=True, null=True)
    child6_dob = models.CharField(max_length=255, blank=True, null=True)

    past_due_cash_medical_support_payperiod = models.CharField(
        max_length=255, blank=True, null=True)
    current_spousal_support_payperiod = models.CharField(
        max_length=255, blank=True, null=True)
    past_due_spousal_support_payperiod = models.CharField(
        max_length=255, blank=True, null=True)
    other_order_payperiod = models.CharField(
        max_length=255, blank=True, null=True)
    total_amount_to_withhold_payperiod = models.CharField(
        max_length=255, blank=True, null=True)
    current_child_support_payperiod = models.CharField(
        max_length=255, blank=True, null=True)
    past_due_child_support_payperiod = models.CharField(
        max_length=255, blank=True, null=True)
    current_cash_medical_support_payperiod = models.CharField(
        max_length=255, blank=True, null=True)

    current_child_support_amt = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    past_due_cash_medical_support = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    total_amt_to_withhold = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    lump_sum_payment_amt = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    disposable_income_percentage = models.CharField(
        max_length=255, blank=True, null=True)
    current_spousal_support = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    other_order_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    ordered_amount_per_weekly = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    ordered_amount_per_biweekly = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    ordered_amount_per_monthly = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    ordered_amount_per_semimonthly = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    final_payment_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    past_due_child_support = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    past_due_spousal_support = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    current_cash_medical_support = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)

    termination_date = models.CharField(max_length=255, blank=True, null=True)
    tribal_payee = models.CharField(max_length=255, blank=True, null=True)
    income_withholding_order = models.CharField(
        max_length=255, blank=True, null=True)
    arrears_greater_than_12_weeks = models.CharField(
        max_length=255, blank=True, null=True)
    one_time_order = models.CharField(max_length=255, blank=True, null=True)
    termination_of_iwo = models.CharField(
        max_length=255, blank=True, null=True)
    amended_iwo = models.CharField(max_length=255, blank=True, null=True)
    never_employed_no_income = models.CharField(
        max_length=255, blank=True, null=True)
    not_currently_employed = models.CharField(
        max_length=255, blank=True, null=True)
    child_support_agency = models.CharField(
        max_length=255, blank=True, null=True)
    court = models.CharField(max_length=255, blank=True, null=True)
    attorney = models.CharField(max_length=255, blank=True, null=True)
    private_individual = models.CharField(
        max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.employee_name} - {self.case_id}"

    class Meta:
        indexes = [
            models.Index(fields=['id'])
        ]
        db_table = "withholding_order_data"




class garnishment_batch_data(models.Model):
    # employee_case = models.OneToOneField(
    #     employee_batch_data,
    #     to_field='case_id',
    #     on_delete=models.CASCADE,
    #     related_name='garnishment_data'
    # )
    ee_id = models.CharField(max_length=255)
    case_id = models.CharField(max_length=255, unique=True)
    garnishment_type = models.CharField(max_length=255)
    ordered_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    arrear_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    current_medical_support = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    past_due_medical_support = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    current_spousal_support = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    past_due_spousal_support = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['ee_id']),
            models.Index(fields=['ee_id', 'case_id']),
        ]
        db_table = "garnishment_batch_data"



class garnishment_order(models.Model):
    # employee = models.ForeignKey(
    #     employee_detail, on_delete=models.CASCADE, related_name="garnishments")
    # employer = models.ForeignKey(Employer_Profile, on_delete=models.SET_NULL,
    #                              null=True, blank=True, related_name="garnishments")
    eeid = models.CharField(max_length=254)
    fein = models.CharField(max_length=254)
    case_id = models.CharField(max_length=255, null=True, blank=True)
    work_state = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    sdu = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(max_length=255, null=True, blank=True)
    end_date = models.DateField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    arrear_greater_than_12_weeks = models.BooleanField(
        default=False, blank=False)
    arrear_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    record_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['eeid']),
            models.Index(fields=['case_id']),
            models.Index(fields=['case_id', 'eeid']),
        ]
        db_table = "garnishment_order"