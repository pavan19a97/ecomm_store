from django.test import Client, RequestFactory, TestCase
from django.shortcuts import redirect
from django.urls import reverse


class CartViewsTestCases(TestCase):
    def setUp(self):
        self.c = Client()
        self.factory = RequestFactory()
    def test_cart_detail(self):
        response = self.c.get(reverse("cart"))
        self.assertEqual(response.status_code, 200)
        response = self.c.get("cart/?remove_from_cart=1")
        self.assertEqual(response.status_code, 404)
    def test_checkout(self):
        response = self.c.get(reverse("checkout"))
        self.assertEqual(response.status_code, 302)