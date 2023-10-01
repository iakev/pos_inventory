from rest_framework.test import APITestCase
from pos_inventory.users.models import User
from django.test import Client
from django.urls import reverse



class TestSetUp(APITestCase):
    """Basic setup for the testcases"""

    def authenticate_user(self) -> None:
        """authenticate a user before each test"""
        user = User.objects.create_user(username="testuser", password="password")
        superuser = User.objects.create_superuser(
            username="adminuser", email="admin@example.com", password="adminpassword"
        )
        import pdb
        pdb.set_trace()
        client, super_client = Client(), Client()
        client.login(username="testuser", password="password")
        super_client.login(username="adminuser", password="adminpassword")
        return client, super_client

    def setUp(self) -> None:
        self.auth_user, self.super_user = self.authenticate_user()
        self.product_url = reverse("products-list")
        self.category_url = reverse("categories-list")
        self.product_data = {
            "name": "Apple",
            "code": "123",
            "description": "European star grape apple",
            "product_type": "1",
            "tax_type": "D",
            "unit": "NO",
            "packaging_unit": "BA",
        }
        self.category_data = {"name": "products"}
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
