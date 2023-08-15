from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    """Basic setup for the testclasses"""

    def setUp(self) -> None:
        self.business_url = reverse("business-list")
        self.suplier_data = {
            "name": "genstores",
            "address": "Murunyi road",
            "email_address": "tests@tester.com",
            "tax_pin": 36727348178,
        }
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()
