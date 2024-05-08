from django.urls import path,re_path
from .import views

urlpatterns = [
    path('GET/api/vendors',views.getVendor), # working
    path('GET/api/vendors/<uuid:pk>/',views.getVendorDetail), # working
    path('POST/api/vendors/',views.addVendor),
    path('PUT/api/vendors/<uuid:pk>/',views.updateVendor),
    path('DELETE/api/vendors/<uuid:pk>/',views.deleteVendor),
    path('POST/api/purchase_order/',views.addPurchaseorder),
    path('GET/api/purchase_order/',views.getPurchaseorder),
    path('GET/api/purchase_order/<uuid:pk>',views.getPurchaseorderDetail),
    path('PUT/api/purchase_order/<uuid:pk>',views.updatePurchaseorder),
    path('DELETE/api/purchase_order/<uuid:pk>',views.deletePurchaseorder),
    re_path('login',views.login),
    re_path('signup',views.signup),
    re_path('test_token',views.test_token),
]



