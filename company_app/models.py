from django.db import models
from master_app.models import Country, State, City  # import from your master_app

class Firms(models.Model):
    # Account & Auth Info
    account_id = models.CharField(max_length=100, unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # use hashed password with proper security
    temp_password = models.CharField(max_length=128, null=True, blank=True) # unhashed
    login_status = models.BooleanField(default=False)

    # Basic Firm Info
    firm_logo = models.ImageField(upload_to='logos/', null=True, blank=True)
    firm_name = models.CharField(max_length=255)
    firm_weburl = models.URLField(blank=True, null=True)
    official_emailid = models.EmailField()
    email_otp = models.CharField(max_length=6, blank=True, null=True)
    email_otp_status = models.BooleanField(default=False)
    contact_number = models.CharField(max_length=15)
    mobile_otp = models.CharField(max_length=6, blank=True, null=True)
    mobile_otp_status = models.BooleanField(default=False)

    # Address Info (relational)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    address = models.TextField()

    status = models.IntegerField(default=0)  # Add this line

    # System Fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "firm"

    def __str__(self):
        return self.firm_name

class BusinessInformation(models.Model):
    account_id = models.OneToOneField(Firms, on_delete=models.CASCADE, to_field='account_id', db_column='account_id', related_name='business_info')

    # Business structure info
    firm_type = models.CharField(max_length=100)
    firm_registration_type = models.CharField(max_length=100, verbose_name="Firm Registration Type")
    about_firm = models.TextField(blank=True, null=True)

    # Registration document
    registration_certificate = models.FileField(upload_to='certificates/', null=True, blank=True)

    # PAN Info
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    pan_front = models.FileField(upload_to='pan_docs/', blank=True, null=True)
    pan_back = models.FileField(upload_to='pan_docs/', blank=True, null=True)

    # Aadhaar Info
    aadhaar_number = models.CharField(max_length=12, blank=True, null=True)
    aadhaar_front = models.FileField(upload_to='aadhaar_docs/', blank=True, null=True)
    aadhaar_back = models.FileField(upload_to='aadhaar_docs/', blank=True, null=True)

    # Tax Info
    tax_type = models.CharField(max_length=50, choices=[('GST', 'GST'), ('Non GST', 'Non GST')])
    gst_number = models.CharField(max_length=20, blank=True, null=True)
    gst_certificate = models.FileField(upload_to='gst_docs/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "business_information"

    def __str__(self):
        return f"{self.account_id.firm_name} - Business Info"

class BusinessOwner(models.Model):
    account_id = models.OneToOneField(Firms, on_delete=models.CASCADE, to_field='account_id', db_column='account_id', related_name='business_owner_info')

    owner_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    email_id = models.EmailField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "business_owner"

    def __str__(self):
        return f"{self.owner_name} ({self.account_id.firm_name})"
    
