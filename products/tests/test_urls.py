from .test_setup import TestSetUp
from django.contrib.auth.models import User
from django.test import Client
import pytest


class TestUrls(TestSetUp):
    def test_products_cannot_be_created_before_authentication(self):
        """Test that a warning is given when we try to fetch the business
        endpoint without authentication
        """
        res = self.client.post(self.product_url)
        assert "Authentication credentials were not provided." in str(res.content)

    @pytest.mark.django_db
    def test_products_can_be_created_after_authentication(self):
        """Test that a business can be created after authentication"""
        cat_response = self.super_user.post(self.category_url, self.category_data, format="json")
        import pdb
        pdb.set_trace()
        res = self.auth_user.post(self.product_url, self.product_data, format="json")
        assert res.content
