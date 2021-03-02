from django.urls import path
from apps.vendor import views
urlpatterns = [
    path("home/", views.vendor_admin, name = 'vendor_home'),
    path("addproduct/", views.add_product, name='vendor_addproduct'),
]