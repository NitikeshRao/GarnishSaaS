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
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.utils import timezone
import time
import os

def index(request, viewtype):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                # Extract form data
                firm_logo = request.FILES.get('firm_logo')
                firm_name = request.POST.get('firm_name')
                firm_weburl = request.POST.get('firm_weburl', None)
                official_emailid = request.POST.get('official_emailid')
                contact_number = request.POST.get('contact_number')
                country_id = request.POST.get('country')
                state_id = request.POST.get('state')
                city_id = request.POST.get('city')
                address = request.POST.get('address')

                # Get the Country, State, City instances
                country = Country.objects.get(id=country_id)
                state = State.objects.get(id=state_id)
                city = City.objects.get(id=city_id)

                firm_type = request.POST.get('firm_type')
                firm_registration_type = request.POST.get('firm_registration_type')
                about_firm = request.POST.get('about_firm', None)

                # Business Owner Data
                owner_name = request.POST.get('owner_name')
                owner_contact_number = request.POST.get('owner_contact_number')
                owner_email = request.POST.get('owner_email')

                # Document fields
                doc_type = request.POST.get('doc_type')
                pan_number = request.POST.get('pan_number') if doc_type == 'PAN' else None
                aadhaar_number = request.POST.get('aadhaar_number') if doc_type == 'AADHAAR' else None
                pan_front = request.FILES.get('pan_front') if doc_type == 'PAN' else None
                pan_back = request.FILES.get('pan_back') if doc_type == 'PAN' else None
                aadhaar_front = request.FILES.get('aadhaar_front') if doc_type == 'AADHAAR' else None
                aadhaar_back = request.FILES.get('aadhaar_back') if doc_type == 'AADHAAR' else None
                registration_certificate = request.FILES.get('reg_certificate') if doc_type not in ['PAN', 'AADHAAR'] else None

                # Tax Type fields
                tax_type = request.POST.get('tax_type')
                gst_number = request.POST.get('gst_number') if tax_type == 'GST' else None
                gst_certificate = request.FILES.get('reg_certificate') if tax_type == 'GST' else None

                # Validate required fields
                if not firm_name or not official_emailid or not contact_number:
                    raise ValidationError("Firm name, email, and contact number are required.")

                # Create the Firm instance
                firm = Firms.objects.create(
                    account_id=settings.APPLICATION_ID,
                    username=firm_name,
                    password=settings.HASHED_TEMP_PASSWORD,
                    temp_password=settings.TEMP_PASSWORD,  # unhashed password
                    firm_logo=firm_logo,
                    firm_name=firm_name,
                    firm_weburl=firm_weburl,
                    official_emailid=official_emailid,
                    email_otp=settings.EMAIL_OTP,
                    contact_number=contact_number,
                    mobile_otp=settings.MOBILE_OTP,
                    country=country,
                    state=state,
                    city=city,
                    address=address
                )

                # Create the Business Information instance
                business_info = BusinessInformation.objects.create(
                    account_id=firm,
                    firm_type=firm_type,
                    firm_registration_type=firm_registration_type,
                    about_firm=about_firm,
                    pan_number=pan_number,
                    pan_front=pan_front,
                    pan_back=pan_back,
                    aadhaar_number=aadhaar_number,
                    aadhaar_front=aadhaar_front,
                    aadhaar_back=aadhaar_back,
                    registration_certificate=registration_certificate,
                    tax_type=tax_type,
                    gst_number=gst_number,
                    gst_certificate=gst_certificate
                )

                # Create the Business Owner instance
                business_owner = BusinessOwner.objects.create(
                    account_id=firm,
                    owner_name=owner_name,
                    contact_number=owner_contact_number,
                    email_id=owner_email
                )

                messages.success(request, 'Company / Firm registered successfully.')
                return redirect('companies', viewtype='list')

            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
                return redirect('companies', viewtype='list')

        else:
            countries = Country.objects.filter(status=1)
            states = State.objects.filter(country_id=101)

            firms = Firms.objects.select_related('state').select_related('city').order_by('-id')
            paginator = Paginator(firms,50)
            page_number = request.GET.get('page')
            page_final_data = paginator.get_page(page_number)            
            totalPageNumber = page_final_data.paginator.num_pages
            current_page = int(request.GET.get('page', 1))

            active_firms = Firms.objects.filter(status=1).count()
            inactive_firms = Firms.objects.filter(status=0).count()

            todaydate = timezone.localdate()
            todays_firms = Firms.objects.filter(created_at__date=todaydate).count()

            data = {
                'data_count':firms,                     
                'binding_data':page_final_data, 
                'current_page':current_page,
                'totalPageNumber':totalPageNumber,
                'totalPageList' : [n+1 for n in range(totalPageNumber)],
                'countries': countries,
                'states': states,
                'viewtype': viewtype,

                'active_firms': active_firms,
                'inactive_firms': inactive_firms,
                'todays_firms': todays_firms,
            }
            return render(request,'company-app/index.html', data)
    else:
        return HttpResponseRedirect(reverse('secure-login'))
    
def editFirm(request, id):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            try:
                # Fetch the existing firm instance
                firm = get_object_or_404(Firms, id=id)

                # Extract form data
                firm_logo = request.FILES.get('firm_logo', firm.firm_logo)
                firm_name = request.POST.get('firm_name')
                firm_weburl = request.POST.get('firm_weburl', firm.firm_weburl)
                official_emailid = request.POST.get('official_emailid')
                contact_number = request.POST.get('contact_number')
                country_id = request.POST.get('country')
                state_id = request.POST.get('state')
                city_id = request.POST.get('city')
                address = request.POST.get('address')

                # Get related location instances
                country = Country.objects.get(id=country_id)
                state = State.objects.get(id=state_id)
                city = City.objects.get(id=city_id)

                # Update firm basic data
                firm.firm_logo = firm_logo
                firm.firm_name = firm_name
                firm.username = firm_name  # assuming username = firm_name
                firm.firm_weburl = firm_weburl
                firm.official_emailid = official_emailid
                firm.contact_number = contact_number
                firm.country = country
                firm.state = state
                firm.city = city
                firm.address = address
                firm.save()

                # Business Info
                business_info, _ = BusinessInformation.objects.get_or_create(account_id=firm)
                business_info.firm_type = request.POST.get('firm_type')
                business_info.firm_registration_type = request.POST.get('firm_registration_type')
                business_info.about_firm = request.POST.get('about_firm')

                doc_type = request.POST.get('doc_type')
                if doc_type == 'PAN':
                    business_info.pan_number = request.POST.get('pan_number')
                    business_info.pan_front = request.FILES.get('pan_front', business_info.pan_front)
                    business_info.pan_back = request.FILES.get('pan_back', business_info.pan_back)
                elif doc_type == 'AADHAAR':
                    business_info.aadhaar_number = request.POST.get('aadhaar_number')
                    business_info.aadhaar_front = request.FILES.get('aadhaar_front', business_info.aadhaar_front)
                    business_info.aadhaar_back = request.FILES.get('aadhaar_back', business_info.aadhaar_back)
                else:
                    business_info.registration_certificate = request.FILES.get('reg_certificate', business_info.registration_certificate)

                tax_type = request.POST.get('tax_type')
                business_info.tax_type = tax_type
                if tax_type == 'GST':
                    business_info.gst_number = request.POST.get('gst_number')
                    business_info.gst_certificate = request.FILES.get('reg_certificate', business_info.gst_certificate)

                business_info.save()

                # Business Owner Info
                business_owner, _ = BusinessOwner.objects.get_or_create(account_id=firm)
                business_owner.owner_name = request.POST.get('owner_name')
                business_owner.contact_number = request.POST.get('owner_contact_number')
                business_owner.email_id = request.POST.get('owner_email')
                business_owner.save()

                messages.success(request, 'Firm details updated successfully.')
                return redirect('edit-company', id=id)

            except Exception as e:
                messages.error(request, f"Error updating firm: {str(e)}")
                return redirect('edit-company', id=id)

        else:           

            firm_info = Firms.objects.select_related('country', 'state', 'city', 'business_info', 'business_owner_info').get(pk=id)

            countries = Country.objects.filter(status=1)
            states = State.objects.filter(country_id=firm_info.country.id)
            cities = City.objects.filter(state_id=firm_info.state.id)

            data = {
                'firm_info':firm_info, 
                'countries': countries,
                'states': states,
                'cities': cities,
            }
            return render(request,'company-app/edit.html', data)
    else:
        return HttpResponseRedirect(reverse('secure-login'))