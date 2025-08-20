# app/urls/employer_urls.py
from django.urls import path
from garnish_processing_app.views import (
    GarnishmentFeesRules
)

app_name = 'garnishment_fees'

urlpatterns = [

  #CRUD for the Garnishment fees rules
  path('fees-rules/<str:rule>/',
       GarnishmentFeesRules.as_view(), name='fees_rules'),
  path('fees-rules/', GarnishmentFeesRules.as_view(), name='fees_rules'),


]
