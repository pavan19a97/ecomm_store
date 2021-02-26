from django.test import TestCase
from django.shortcuts import reverse

from temp.models import Category, Product, User

class TestCaseCategory(TestCase):

    def setUp(self):
        self.data1  = Category.objects.create(title='chairs', slug='chairs')


    def test_category_model_entry(self):
        """
        Test Category model data insertion/types/field attributes
        """

        data = self.data1
        self.assertTrue(isinstance(data, Category))
        self.assertEqual(str(data), 'chairs')


class TestProductsModel(TestCase):
    def setUp(self):
        category = Category.objects.create(title='django', slug='django')
        user = User.objects.create(username='admin', is_vendor=True)
        self.data1 = Product.objects.create(category=category, title='django beginners', vendor= user,
                                            slug='django-beginners', price='20.00', image='django')
        self.data2 = Product.objects.create(category=category, title='django advanced', vendor= user,
                                             slug='django-advanced', price='20.00', image='django')

    def test_products_model_entry(self):
        """
        Test product model data insertion/types/field attributes
        """
        data = self.data1
        self.assertTrue(isinstance(data, Product))
        self.assertEqual(str(data), 'django beginners')

    # def test_products_url(self):
    #     """
    #     Test product model slug and URL reverse
    #     """
    #     data = self.data1
    #     url = reverse('store:product_detail', args=[data.slug])
    #     self.assertEqual(url, '/item/django-beginners/')
    #     response = self.client.post(
    #         reverse('store:product_detail', args=[data.slug]))
    #     self.assertEqual(response.status_code, 200)

    def test_products_custom_manager_basic(self):
        """
        Test product model custom manager returns only active products
        """
        data = Product.objects.all()
        self.assertEqual(data.count(), 2)