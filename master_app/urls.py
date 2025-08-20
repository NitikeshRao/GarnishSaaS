from django.urls import path, include
from master_app import views

urlpatterns = [
    #======================== Home Manager ========================
    path('', views.index, name='dashboard'),

    #======================== Company Manager ========================

    path('company/', include('company_app.urls')),

    #======================== Garnish Processing Manager ========================

    path('garnish-process/', include('garnish_processing_app.urls')),

    #======================== ADDONS ROUTES ========================

    path('get_states/', views.getStates, name='get_states'),
    path('get_cities/', views.getCities, name='get_cities'),
    
    #======================== Settings Manager ========================

    # -------- GENERAL SETTINGS --------
    path('settings/general', views.generalSettings, name='general-settings'),
    path('settings/social', views.socialPagesSettings, name='social-pages-settings'),
    path('settings/maintenance', views.maintenanceSettings, name='maintenance-settings'),

    # -------- SYSTEM SETTINGS --------
    path('settings/smtp-configuration', views.systemSettings, name='system-settings'),

    # -------- GOOGLE SETTINGS --------
    path('settings/recaptcha-configuration', views.googleSettings, name='google-settings'),

    #======================== Account Manager ========================

    path('account/change-password', views.changePassword, name='change-password'),
]
