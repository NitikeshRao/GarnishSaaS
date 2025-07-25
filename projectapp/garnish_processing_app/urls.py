from django.urls import path, include
from garnish_processing_app import views

urlpatterns = [
    #======================== Home Manager ========================
    path('', views.index, name='garnish-employee-calculator'),
]
