from django.test import TestCase


from unittest import skip

from django.contrib.auth.models import User
from django.http import HttpRequest
from django.test import Client, RequestFactory, TestCase
from django.shortcuts import redirect
from django.urls import reverse

from temp.models import Category, Product, User
from temp import views
from temp.forms import UserForm, ProductForm, AddToCartForm

class TestCaseViews(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
        user = User.objects.create(username='admin')
        category = Category.objects.create(title = 'django', slug = 'django')
        data1 = Product.objects.create(category=category, title='django beginners', vendor=user,
                                            slug='django-beginners', price='20.00', image='django',
                                            thumbnail='django_thumb')

    def test_url_allowed_hosts(self):
        """
        Test allowed hosts
        """
        response = self.c.get('/', HTTP_HOST='noaddress.com')
        self.assertEqual(response.status_code, 400)
        response = self.c.get('/', HTTP_HOST='127.0.0.1:8000')
        self.assertEqual(response.status_code, 400)

    def test_homepage_url(self):
        """
        Test homepage response status
        """
        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        user = User.objects.create_user(username = "pavan", email="emai@gmail.com", is_vendor = True)

        response = self.c.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.c.get('/?page=1')
        self.assertEqual(response.status_code, 200)
        response = self.c.get('/?max = 100&min=10')

        self.assertEqual(response.status_code, 200)
        # request = self.factory.post(reverse('ecomm_home'), {})
        # request.user = user
        # print(request.user.is_anonymous)
        # response = views.ecomm_home(request)
    def test_views_register(self):
        userform = UserForm()
        self.assertEqual(userform, userform)
        response = self.c.get(reverse('sign_up'), {'u_form': UserForm})
        self.assertEqual(response.status_code, 200)

        response = self.c.post(reverse('sign_up'), args={"email":"pavan@gmail.com",'username':'admin', 'password':'pass'})
        self.assertEqual(response.status_code, 200)

        request = RequestFactory().get('/signup',{'u_form':UserForm})
        response = self.c.get('/signup')
        UserForm(request.POST, request.FILES)
        self.assertEqual(response.status_code, 301)
    def test_views_search(self):
        response = self.c.get('/search/?query="this"')
        self.assertEqual(response.status_code, 200)

        response= self.c.get(('/product/django/django-beginners'),args={"category_slug":"django", "product_slug":"django-beginners"})

        self.assertEqual(response.status_code, 301)