# app/urls/employer_urls.py
from django.urls import path
from processor.views import (
    GarnishmentFeesRulesAPI, GarnishmentFeesListByFilterAPI
)

app_name = 'gar_fees'

urlpatterns = [

  #CRUD for the Garnishment fees rules
  path('rules/<str:rule>/',
       GarnishmentFeesRulesAPI.as_view(), name='fees_rules'),
  path('rules/', GarnishmentFeesRulesAPI.as_view(), name='fees_rules'),

  path(
        "rules/filter/<str:state>/<str:pay_period>/<str:garnishment_type/",
        GarnishmentFeesListByFilterAPI.as_view(),
        name="garnishment-fees-filter",
    ),


]
