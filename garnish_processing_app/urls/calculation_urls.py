from django.urls import path

from garnish_processing_app.views.calculation_views import PostCalculationView

app_name = 'garnishment'

urlpatterns = [


 # Garnishment calculation for api all types
    path('calculate/', PostCalculationView.as_view(), name='calculate')
    
    

]