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
            return HttpResponse('hello')
        else:
            return render(request,'garnish-process-app/index.html')
    else:
        return HttpResponseRedirect(reverse('secure-login'))