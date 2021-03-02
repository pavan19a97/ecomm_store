from django.urls import path
from apps.product import views
urlpatterns = [
    path('<slug:category_slug>/<slug:product_slug>/', views.product,name ='product'),
]