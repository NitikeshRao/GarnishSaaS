# garnish_processing_app/urls/garnishment_urls.py
from django.urls import path
from garnish_processing_app import views
from garnish_processing_app.views import ConvertExcelToJsonView
app_name = 'garnish_processing_app'

urlpatterns = [
    # Garnishment Calculator
    path('', views.index, name='garnishment-calculator'),

    # Batch Processing Manager
    # path('batch', ConvertExcelToJsonView.as_view(), name='batch'),
    path('batch-processing', ConvertExcelToJsonView.as_view(), name='batch-processing'),

    # Rules Manager
    path('child-support-rules', views.childSupportRules, name='child-support-rules'),
    path('state-tax-levy-rules', views.stateTaxLevyRules, name='state-tax-levy-rules'),
    path('creditor-dept-rules', views.creditorDeptRules, name='creditor-dept-rules'),
]
