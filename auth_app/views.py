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
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator
from django.shortcuts import render
from django.urls import reverse
import time
import os

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        if request.method =='POST':        
            Security_Code = request.POST['Security_Code']
            Security_Password = request.POST['Secure_Password']
            
            user = authenticate(username=Security_Code, password=Security_Password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged In Successfully')            
                return HttpResponseRedirect(reverse('dashboard'))
            else:
                messages.error(request, 'Invalid Credentials, please try again')
                return HttpResponseRedirect(reverse('secure-login'))          
        return render(request,'auth/index.html')

def twoFactorVerification(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return render(request, 'auth/two-factor-verification.html')
        
def forgotPassword(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dashboard'))
    else:
        return render(request, 'auth/forgot-password.html')
    
def secureLogout(request):
    logout(request)
    messages.success(request, 'Logout Successfully')
    return HttpResponseRedirect(reverse('secure-login'))