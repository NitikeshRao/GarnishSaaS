from django.urls import path
from auth_app import views

urlpatterns = [
    path('', views.index, name='secure-login'),
    path('two-factor-verification', views.twoFactorVerification, name='two-factor-verification'),
    path('forgot-password', views.forgotPassword, name='forgot-password'),
    path('secure-logout',views.secureLogout, name='secure-logout'),
]