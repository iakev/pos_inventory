from .test_setup import TestSetUp
from django.urls import reverse
import pytest


class TestSaleUrls(TestSetUp):
    def test_payment_cannot_be_created_before_authentication(self):
        """Test that a warning is given when we try to fetch the payment
        mode endpoint without authentication
        """
        res = self.client.post(self.payment_mode_url)
        assert "Authentication credentials were not provided." in str(res.content)

    @pytest.mark.django_db
    def test_payment_can_be_created_after_authentication(self):
        """Test that a business can be created after authentication"""
        res = self.auth_user.post(self.payment_mode_url, self.payment_mode_data1, format="json")
        assert self.payment_mode_data1["payment_method"] == res.json()["payment_method"]

    def test_payment_mode_can_be_retrieved_as_list(self):
        """Tests a list of all paymentmode can be retrieved"""
        self.auth_user.post(self.payment_mode_url, self.payment_mode_data1, format="json")
        self.auth_user.post(self.payment_mode_url, self.payment_mode_data2, format="json")
        res = self.auth_user.get(self.payment_mode_url)
        assert len(res.json()) == 2

    def test_payment_mode_can_be_edited_after_creation(self):
        """Test that the put method works and a payment mode can be edited"""
        res = self.auth_user.post(self.payment_mode_url, self.payment_mode_data1, format="json")
        uuid = res.json()["uuid"]
        payment_mode_url = reverse("paymentmodes-detail", args=[uuid])
        res = self.auth_user.put(payment_mode_url, {"payment_method": "01"}, content_type="application/json")
        assert res.json()["payment_method"] == "01"

    def test_payment_mode_can_be_deleted(self):
        """Test that a specific instance of the payment mode can be deleted"""
        original_res = self.auth_user.post(self.payment_mode_url, self.payment_mode_data1, format="json")
        uuid = original_res.json()["uuid"]
        payment_mode_url = reverse("paymentmodes-detail", args=[uuid])
        self.auth_user.delete(payment_mode_url)
        res = self.auth_user.get(self.payment_mode_url)
        assert original_res.json() != res.json() and res.json() == []

    def test_payment_mode_single_property_can_be_edited(self):
        """Test that a single property of the payment mode can be changed"""
        original_res = self.auth_user.post(self.payment_mode_url, self.payment_mode_data1, format="json")
        uuid = original_res.json()["uuid"]
        payment_mode_url = reverse("paymentmodes-detail", args=[uuid])
        res = self.auth_user.patch(payment_mode_url, {"payment_method": "04"}, content_type="application/json")
        assert original_res.json() != res.json() and res.json()["payment_method"] == "04"
