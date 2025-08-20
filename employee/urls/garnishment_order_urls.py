# app/urls/employer_urls.py
from django.urls import path

from employee.views.garnishment_order_views import GarnishmentOrderDetails,UpsertGarnishmentOrderView,ExportGarnishmentOrderDataView,GarnishmentOrderImportView

app_name = 'order'

urlpatterns = [


    # CRUD for the garnishment order
    path('order-details/', GarnishmentOrderDetails.as_view(), name='order_details'),
    path('order-details/<str:case_id>/',
         GarnishmentOrderDetails.as_view(), name='delete_order'),

    # Import Order using excel
    path('import-orders/', GarnishmentOrderImportView.as_view(), name='import_orders'),


    # Insert+Update order details using excel
    path('upsert-orders/', UpsertGarnishmentOrderView.as_view(), name='upsert_orders'),

    # Export garnishment order data in excel
    path('export/', ExportGarnishmentOrderDataView.as_view(),
         name='export_orders'),

]
