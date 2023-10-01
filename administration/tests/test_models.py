from .test_setup import TestSetUp
from django.contrib.auth.models import User
from django.test import Client
import pytest


class TestModels(TestSetUp):
    def test_business_cannot_be_created_before_authentication(self):
        """Test that a warning is given when we try to fetch the business
        endpoint without authentication
        """
        res = self.client.post(self.business_url)
        assert "Authentication credentials were not provided." in str(res.content)

    @pytest.mark.django_db
    def test_business_can_be_created_after_authentication(self):
        """Test that a business can be created after authentication"""
        res = self.auth_user.post(self.business_url, self.supplier_data, format="json")
        assert  res.content
