from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [   
    path('', include('website.urls')),
    path('auth/', include('auth_app.urls')),
    path('app/master/', include('master_app.urls')),
    #path('admin/', admin.site.urls),
    path('__reload__/', include('django_browser_reload.urls')),
    path(
        'garnish-process/',
        include(('garnish_processing_app.urls', 'garnish_processing_app'))

    ),
    path('processor/', include('processor.urls.garnishment_types.calculation_urls','processor')),
    path('exempt_amt/', include('processor.urls.configs.exempt_urls','exempt_amt')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)