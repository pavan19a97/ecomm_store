from django.urls import path
from apps.core import views
urlpatterns = [
    path('search/', views.search, name= 'search'),
    path("", views.home, name="ecommstore_home"),
    path("signup/", views.register, name="sign_up"),

    path('<slug:category_slug>/', views.category, name='category'),

]