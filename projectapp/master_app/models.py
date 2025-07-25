from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class GeneralSetting(models.Model):
    id =models.AutoField(primary_key=True,auto_created=True)
    keytitle =models.CharField(max_length=255)
    value =models.TextField(null=True)
    status=models.PositiveSmallIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)  # timestamp, updated automatically
    class Meta:
        db_table="general_setting"
    def __str__(self):
        return self.keytitle

# When change default data need to run 2 commands
# python manage.py migrate master_app 0001
# python manage.py migrate master_app

class Country(models.Model):
    code = models.CharField(max_length=10, unique=True, default='TEMP')
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=1, choices=[('0', 'Inactive'), ('1', 'Active')], default='1')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)  # Soft delete field

    class Meta:
        db_table = "country"

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=255)
    country = models.ForeignKey('Country', on_delete=models.CASCADE)
    status = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)  # Soft delete field

    class Meta:
        db_table = "state"

    def __str__(self):
        return self.name

class City(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    state = models.ForeignKey('State', on_delete=models.CASCADE)
    status = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now=True)  # Soft delete field

    class Meta:
        db_table = "city"

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    account_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    emailotp = models.CharField(max_length=6, blank=True, null=True)
    emailotp_status = models.CharField(max_length=1, choices=[('0', 'Not Verified'), ('1', 'Verified')], default='0')
    mobilenumber = models.CharField(max_length=15, unique=True, null=True, blank=True)
    mobotp = models.CharField(max_length=6, blank=True, null=True)
    mobilenum_status = models.CharField(max_length=1, choices=[('0', 'Not Verified'), ('1', 'Verified')], default='0')
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], blank=True, null=True)
    countryId = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    stateId = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    cityId = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    fcm_key = models.CharField(max_length=255, blank=True, null=True)
    notification_status = models.CharField(max_length=1, choices=[('0', 'Off'), ('1', 'On')], default='1')
    status = models.CharField(max_length=1, choices=[('0', 'Inactive'), ('1', 'Active')], default='1')
    live_status = models.CharField(max_length=1, choices=[('0', 'Offline'), ('1', 'Online')], default='0')

    class Meta:
        db_table = 'customuser'  # This is the new table name without the 'master_app_' prefix
