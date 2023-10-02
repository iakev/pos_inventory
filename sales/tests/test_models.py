from django.db.utils import IntegrityError
from sales.models import PaymentMode
from django.test import TestCase
import pytest


class PaymentModeTestCase(TestCase):
    def setUp(self):
        # Create an instance of PaymentMode for testing
        self.payment_mode = PaymentMode.objects.create(
            payment_method=PaymentMode.PaymentMethod.CASH, properties={"key": "value"}
        )

    def tearDown(self):
        # Perform any cleanup actions here, such as deleting test objects
        self.payment_mode.delete()

    def test_str_method(self):
        """
        Test the __str__ method of the PaymentMode model.
        """
        expected_str = "CASH"
        assert str(self.payment_mode) == expected_str

    def test_payment_method_choices(self):
        """
        Test that the payment method is within the available choices.
        """
        choices = dict(PaymentMode.PaymentMethod.choices)
        assert self.payment_mode.payment_method in choices.keys()

    def test_payment_method_labels(self):
        """
        Test that the __str__ method returns the expected payment method labels.
        """
        expected_labels = {
            PaymentMode.PaymentMethod.CASH: "CASH",
            PaymentMode.PaymentMethod.CREDIT: "CREDIT",
            PaymentMode.PaymentMethod.CASH_CREDIT: "CASH/CREDIT",
            PaymentMode.PaymentMethod.BANK_CHECK: "BANK CHECK",
            PaymentMode.PaymentMethod.CARD: "DEBIT AND CREDIT CARD",
            PaymentMode.PaymentMethod.MOBILE_MONEY: "MOBILE MONEY",
            PaymentMode.PaymentMethod.OTHER: "OTHER",
        }
        assert self.payment_mode.__str__() == expected_labels.get(self.payment_mode.payment_method, "")

    def test_default_payment_method(self):
        """
        Test that the default payment method is set correctly.
        """
        payment_mode = PaymentMode.objects.create()
        default_payment_method = PaymentMode.PaymentMethod.CASH
        assert payment_mode.payment_method == default_payment_method

    def test_properties_field(self):
        """
        Test the properties field to ensure it can store JSON data.
        """
        assert self.payment_mode.properties == {"key": "value"}

    def test_that_uuids_are_unique_for_each_instance(self):
        """Test that each payment instance has unique uuid"""
        payment_mode = PaymentMode.objects.create()
        assert payment_mode.uuid != self.payment_mode.uuid
