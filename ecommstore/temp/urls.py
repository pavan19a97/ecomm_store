from django.urls import path
from . import views
urlpatterns = [
    path('search/', views.search, name= 'search'),
    path("", views.home, name="ecommstore_home"),
    path("signup/", views.register, name="sign_up"),
    path("vendorhome/", views.vendor_admin, name = 'vendor_home'),
    path("vendor/addproduct", views.add_product, name='vendor_addproduct'),
    path('product/<slug:category_slug>/<slug:product_slug>/', views.product,name ='product'),
    path('<slug:category_slug>/', views.category, name='category'),

]