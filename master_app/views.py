from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.mail import BadHeaderError, send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import *
from django.db import connection
from django.contrib import messages
from django.shortcuts import redirect
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import default_storage
import time
import os

# Create your views here.
def index(request):    
    if request.user.is_authenticated:           
        return render(request,'master-app/index.html')
    else:
        return HttpResponseRedirect(reverse('secure-login'))


# ADDONS MANAGER

def getStates(request):
    # Get the country id from the GET request
    country_id = request.GET.get('country_id')
    
    # Fetch cities that belong to the selected state
    states = State.objects.filter(country_id=country_id).values('id', 'name')
    
    # Return the cities as JSON
    return JsonResponse(list(states), safe=False)

def getCities(request):
    # Get the state id from the GET request
    state_id = request.GET.get('state_id')
    
    # Fetch cities that belong to the selected state
    cities = City.objects.filter(state_id=state_id).values('id', 'name')
    
    # Return the cities as JSON
    return JsonResponse(list(cities), safe=False)


# SETTINGS MANAGER

# ========== General Settings Manager ==============
def generalSettings(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Text fields
                         
            keys = [
                'company_name', 'app_name', 'contact_numbers', 'contact_emails', 'office_time', 'office_address', 'country', 'state', 'city', 'postal_code', 'login_screen_head_title', 'login_screen_foot_title', 'base_configuration',
            ]

            for key in keys:
                value = request.POST.get(key, '')
                if value != '':
                    GeneralSetting.objects.update_or_create(
                        keytitle=key, defaults={'value': value, 'status': 1}
                    )
            # File uploads
            image_keys = ['login_background', 'white_logo', 'dark_logo', 'mini_logo', 'favicon']
            upload_dir = ''

            for key in image_keys:
                if key in request.FILES:
                    file = request.FILES[key]

                    # Get or create the setting record
                    setting_obj, created = GeneralSetting.objects.get_or_create(keytitle=key)

                    # Delete old file if exists
                    if setting_obj.value:
                        old_path = os.path.join(settings.MEDIA_ROOT, setting_obj.value)
                        if os.path.exists(old_path):
                            os.remove(old_path)

                    # Save file using default storage
                    relative_path = os.path.join(upload_dir, file.name)
                    saved_path = default_storage.save(relative_path, file)

                    # Save relative path to DB (relative to MEDIA_ROOT)
                    setting_obj.value = saved_path
                    setting_obj.status = 1
                    setting_obj.save()
            messages.success(request, 'Updated Successfully...')            
            return HttpResponseRedirect(reverse('general-settings'))
        else:
            return render(request,'master-app/settings/index.html')
    else:
        return HttpResponseRedirect(reverse('secure-login'))

def socialPagesSettings(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Text fields
                         
            keys = [
                'facebook_page', 'twitter_page', 'linkedin_page', 'instagram_page', 'youtube_page', 'socialpages_configuration',
            ]

            for key in keys:
                value = request.POST.get(key, '')
                if value != '':
                    GeneralSetting.objects.update_or_create(
                        keytitle=key, defaults={'value': value, 'status': 1}
                    )
            messages.success(request, 'Updated Successfully...')            
            return HttpResponseRedirect(reverse('social-pages-settings'))
        else:
            return render(request,'master-app/settings/social-pages.html')
    else:
        return HttpResponseRedirect(reverse('secure-login'))

def maintenanceSettings(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Text fields
                         
            keys = [
                'maintenance_message', 'maintenance_mode',
            ]

            for key in keys:
                value = request.POST.get(key, '')
                if value != '':
                    GeneralSetting.objects.update_or_create(
                        keytitle=key, defaults={'value': value, 'status': 1}
                    )
            messages.success(request, 'Updated Successfully...')            
            return HttpResponseRedirect(reverse('maintenance-settings'))
        else:
            return render(request,'master-app/settings/maintenance.html')
    else:
        return HttpResponseRedirect(reverse('secure-login'))

# ========== System Settings Manager ==============
def systemSettings(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Text fields

            keys = [
                'MAIL_DRIVER', 'MAIL_HOST', 'MAIL_PORT', 'MAIL_ENCRYPTION', 'MAIL_USERNAME', 'MAIL_FROM_ADDRESS', 'MAIL_PASSWORD', 'RECEIVING_MAIL', 'mail_configuration',
            ]

            for key in keys:
                value = request.POST.get(key, '')
                if value != '':
                    GeneralSetting.objects.update_or_create(
                        keytitle=key, defaults={'value': value, 'status': 1}
                    )
            messages.success(request, 'Updated Successfully...')            
            return HttpResponseRedirect(reverse('system-settings'))
        else:
            return render(request,'master-app/settings/email-setting.html')
    else:
        return HttpResponseRedirect(reverse('secure-login'))
    
# ========== Google Settings Manager ==============
def googleSettings(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            # Text fields
                         
            keys = [
                'google_recptcha_sitekey', 'google_recptcha_secretkey', 'recptcha_configuration',
            ]

            for key in keys:
                value = request.POST.get(key, '')
                if value != '':
                    GeneralSetting.objects.update_or_create(
                        keytitle=key, defaults={'value': value, 'status': 1}
                    )
            messages.success(request, 'Updated Successfully...')            
            return HttpResponseRedirect(reverse('google-settings'))
        else:
            return render(request,'master-app/settings/google-recptcha-setting.html')
    else:
        return HttpResponseRedirect(reverse('secure-login'))

# ACCOUNT MANAGER

# ========== Password Manager ==============
def changePassword(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            current_password = request.POST['current_password']
            new_password = request.POST['new_password']
            confirm_password = request.POST['confirm_password']
            
            user = User.objects.get(id=request.user.id)
            getusername = user.username
            checkcurrent_password = user.check_password(current_password)

            if checkcurrent_password!=True:
                messages.error(request, 'Invalid current password.')
                return HttpResponseRedirect(reverse('change-password'))
            else:
                if new_password != confirm_password:
                    messages.error(request, 'New passwords not matched.')
                    return HttpResponseRedirect(reverse('change-password'))    
                else:
                    user.set_password(confirm_password)
                    user.save()
                    messages.success(request, 'Password changed successfully.')
                    user = User.objects.get(username=getusername)
                    login(request, user)
                    return HttpResponseRedirect(reverse('change-password'))
        else:
            return render(request,'master-app/account/change-password.html')
    else:
        return HttpResponseRedirect(reverse('secure-login'))