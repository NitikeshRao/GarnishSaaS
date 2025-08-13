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

def index(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of garnishment-calculator')
        else:
            return render(request,'garnish-process-app/index.html')
    else:
        return HttpResponseRedirect(reverse('secure-login'))
    
def batchProcess(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of batch-processing')
        else:
            return render(request,'garnish-process-app/batch-process/index.html')
    else:
        return HttpResponseRedirect(reverse('secure-login'))
    
def childSupportRules(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of child-support-rules')
        else:
            us_states = [
                'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
                'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
                'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
                'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
                'Wisconsin', 'Wyoming'
            ]
            return render(request,'garnish-process-app/garnish-rules/child-support/index.html', {'states': us_states})
    else:
        return HttpResponseRedirect(reverse('secure-login'))
    
def stateTaxLevyRules(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of state-tax-levy-rules')
        else:
            us_states = [
                'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
                'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
                'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
                'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
                'Wisconsin', 'Wyoming'
            ]
            return render(request,'garnish-process-app/garnish-rules/state-tax-levy/index.html', {'states': us_states})
    else:
        return HttpResponseRedirect(reverse('secure-login'))

def creditorDeptRules(request):    
    if request.user.is_authenticated:
        if request.method == 'POST':
            return HttpResponse('i am post method of state-tax-levy-rules')
        else:
            us_states = [
                'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
                'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
                'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
                'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
                'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
                'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
                'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
                'Wisconsin', 'Wyoming'
            ]
            return render(request,'garnish-process-app/garnish-rules/creditor-dept/index.html', {'states': us_states})
    else:
        return HttpResponseRedirect(reverse('secure-login'))