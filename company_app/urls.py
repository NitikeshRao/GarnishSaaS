from django.urls import path
from company_app import views

urlpatterns = [
    #======================== Company Manager ========================
    
    path('<str:viewtype>', views.index, name='companies'),
    path('edit/<int:id>', views.editFirm, name='edit-company'),
]
