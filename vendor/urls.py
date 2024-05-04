from django.urls import path
from .views import vendorView,PurchaseOrdersView,SigninAPI,TokenRefershAPI
urlpatterns = [
    path('login/',SigninAPI.as_view()),
    path('token/refresh/',TokenRefershAPI.as_view()),
    path('vendors/',vendorView.as_view(),name="vendors"),
    path('vendors/<int:vendor_id>/',vendorView.as_view(),name="specificvendor"),
    path('vendors/<int:vendor_id>/performance/',vendorView.as_view(),name="specificvendorperformance"),
    path('purchase_orders/',PurchaseOrdersView.as_view(),name="purchaseorders"),
    path('purchase_orders/<int:po_id>/',PurchaseOrdersView.as_view(),name="specificpurchaseorder"),
    path('purchase_orders/<int:po_id>/acknowledge/',PurchaseOrdersView.as_view(),name="update acknowledgment date for a specific Po"),
]