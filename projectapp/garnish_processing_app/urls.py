from django.urls import path, include
from garnish_processing_app import views

urlpatterns = [
    #======================== Garnishment Calculator Manager ========================
    path('', views.index, name='garnishment-calculator'),

    #======================== Batch Processing Manager ========================
    path('batch-processing', views.batchProcess, name='batch-processing'),

    #======================== Rules Manager ========================
    path('child-support-rules', views.childSupportRules, name='child-support-rules'),
]
