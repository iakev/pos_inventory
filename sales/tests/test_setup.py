from rest_framework.test import APITestCase
from pos_inventory.users.models import User
from django.test import Client
from django.urls import reverse

class TestSetUp(APITestCase):
    """Basic setup for the testcases"""

    def authenticate_user(self) -> None:
        """authenticate a user before each test"""
        User.objects.create_user(username="testuser", password="password")
        client = Client()
        client.login(username="testuser", password="password")
        return client

    def setUp(self) -> None:
        self.auth_user = self.authenticate_user()
        self.payment_mode_url = reverse("paymentmodes-list")
        self.payment_mode_data1 = {"payment_method": "02"}
        self.payment_mode_data2 = {"payment_method": "01"}
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
