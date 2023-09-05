from rest_framework.test import APITestCase
from pos_inventory.users.models import User
from django.test import Client
from django.urls import reverse
from rest_framework.authtoken.models import Token
import pytest


class TestSetUp(APITestCase):
    """Basic setup for the testcases"""

    def authenticate_user(self) -> None:
        """authenticate a user before each test"""
        user = User.objects.create_user(username='testuser', password='password')
        token, _ = Token.objects.get_or_create(user=user)  # Get or create a token for the user
        client = Client()
        client.login(username='testuser', password='password')
        client.defaults['HTTP_AUTHORIZATION'] = f'Token {token.key}'  # Add the token to the headers
        return client

    def setUp(self) -> None:
        self.auth_user = self.authenticate_user()
        self.business_url = reverse("business-list")
        self.supplier_data = {
            "name": "genstores",
            "address": "Murunyi road",
            "email_address": "tests@tester.com",
            "tax_pin": 36727348178,
        }
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
