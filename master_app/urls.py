from django.urls import path, include, re_path
from master_app import views
from .views import ManageEmployeeView, ManageOrderView, ManageClientView, GarnishmentFeesListByFilterAPI

urlpatterns = [
    #======================== Home Manager ========================
    path('', views.index, name='dashboard'),
    
    path('client-list', ManageClientView.as_view(), name='client-list'),
    path('employee-list', ManageEmployeeView.as_view(), name='employee-list'),
    path('order-list', ManageOrderView.as_view(), name='order-list'),

    # path(
    #     'rules/filter/<str:state>/<str:pay_period>/<str:garnishment_type>/',
    #     GarnishmentFeesListByFilterAPI.as_view(),
    #     name="garnishment-fees-filter"
    # ),

    re_path(
        r'^rules/filter(?:/(?P<state>[^/]+))?(?:/(?P<pay_period>[^/]+))?(?:/(?P<garnishment_type>[^/]+))?/$',
        GarnishmentFeesListByFilterAPI.as_view(),
        name="garnishment-fees-filter"
    ),

    #======================== Company Manager ========================

    path('company/', include('company_app.urls')),

    #======================== Garnish Processing Manager ========================

    path('garnish-process/', include('garnish_processing_app.urls')),
    
    #======================== Processor Manager ========================
    
    path('processor/', include('processor.urls')),

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
