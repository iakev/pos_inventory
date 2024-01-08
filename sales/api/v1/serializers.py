"""
Module for creating serializerd for Sales application models
"""
from typing import Any
from decimal import Decimal, ROUND_HALF_EVEN
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from administration.models import Supplier, Employee, Business
from pos_inventory.users.api.serializers import UserResponseSerializerAvecNameSole
from administration.api.v1.serializers import (
    BusinessSerializer,
    EmployeeSerializer,
    EmployeeRestrictedSerializer,
)
from sales.models import (
    PaymentMode,
    ProductSales,
    Sales,
    Customer,
    Purchase,
    PurchaseProduct,
)
from products.models import Product, Stock
from products.api.v1.serializers import (
    ProductSerializer,
    ProductResponseSerializer,
    ProductSansSupplierResponseSerializer,
    SupplierRelatedResponseSerializer,
)
from drf_spectacular.utils import extend_schema_field


class CustomerSerializer(serializers.ModelSerializer):
    """Serializer for Customer model"""

    class Meta:
        model = Customer
        fields = [
            "uuid",
            "created_at",
            "updated_at",
            "name",
            "address",
            "tax_pin",
            "email_address",
        ]


class PaymentModeSerializer(serializers.ModelSerializer):
    """
    Serializer for PaymentMode model Request
    """

    properties = serializers.JSONField(required=False)

    class Meta:
        model = PaymentMode
        fields = ["uuid", "payment_method", "properties"]

    def create(self, validated_data):
        """Create a new payment mode"""
        properties = validated_data.pop(
            "properties", {}
        )  # Get the properties data or an empty dictionary if not provided
        payment_mode = PaymentMode(**validated_data)
        payment_mode.properties = properties
        payment_mode.save()
        return payment_mode

    def update(self, payment, validated_data):
        """Update a payment mode instance"""
        properties_data = validated_data.pop(
            "properties", None
        )  # Get the properties data or an empty dictionary if not provided
        if properties_data:
            payment.properties = properties_data
        payment.payment_method = validated_data.get("mode", payment.payment_method)
        payment.save()
        return payment

    def to_representation(self, instance):
        """
        Delegating representation to make it more user friendly
        with the database values
        """
        return PaymentModeResponseSerializer(context=self.context).to_representation(instance)


class PaymentModeResponseSerializer(serializers.ModelSerializer):
    """
    Payment Mode Response serializer
    """

    payment_method = serializers.CharField(source="get_payment_method_display", read_only=True)

    class Meta:
        model = PaymentMode
        fields = ["uuid", "payment_method"]


class SalesSerializer(serializers.ModelSerializer):
    """
    Serializer for Sales model
    """

    business_uuid = serializers.UUIDField()
    employee_uuid = serializers.UUIDField()
    payment_uuid = serializers.UUIDField()
    customer_uuid = serializers.UUIDField()
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Sales
        fields = [
            "uuid",
            "customer_uuid",
            "business_uuid",
            "payment_uuid",
            "employee_uuid",
            "products",
            "sale_amount_with_tax",
            "tax_amount",
            "receipt_type",
            "transaction_type",
            "receipt_label",
            "sale_status",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        """Validate data by mapping uuids to ids required in database"""
        business_uuid = data.pop("business_uuid", None)
        employee_uuid = data.pop("employee_uuid", None)
        payment_uuid = data.pop("payment_uuid", None)
        customer_uuid = data.pop("customer_uuid", None)
        receipt_type = data.get("receipt_type", None)
        transaction_type = data.get("transaction_type", None)
        validated_data = super().validate(data)
        if employee_uuid:
            employee = get_object_or_404(Employee, uuid=employee_uuid)
            validated_data["employee"] = employee
        if payment_uuid:
            payment = get_object_or_404(PaymentMode, uuid=payment_uuid)
            validated_data["payment"] = payment
        if business_uuid:
            business = get_object_or_404(Business, uuid=business_uuid)
            validated_data["business"] = business
        if customer_uuid:
            customer = get_object_or_404(Customer, uuid=customer_uuid)
            validated_data["customer"] = customer
        if transaction_type and receipt_type:
            validated_data["receipt_label"] = transaction_type + receipt_type
        return validated_data

    def get_receipt_type_db_value(self, human_readable_val):
        """
        Convert receipt type to database value
        """
        receipt_type_choices = Sales.SalesReceiptType.choices
        try:
            receipt_type_choices_dict = dict((y, x) for x, y in receipt_type_choices)
            return receipt_type_choices_dict[human_readable_val]
        except KeyError:
            raise serializers.ValidationError("Invalid receipt_type value")

    def get_transaction_type_db_value(self, human_readable_val):
        """
        Convert transaction_type to database value
        """
        transaction_type_choices = Sales.TransactionType.choices
        try:
            transaction_type_choices_dict = dict((y, x) for x, y in transaction_type_choices)
            return transaction_type_choices_dict[human_readable_val]
        except KeyError:
            raise serializers.ValidationError("Invalid transaction_type value")

    def get_sale_status_db_value(self, human_readable_val):
        """
        Convert sale_status to db value
        """
        sale_status_choices = Sales.TransactionProgress.choices
        try:
            sale_status_choices_dict = dict((y, x) for x, y in sale_status_choices)
            return sale_status_choices_dict[human_readable_val]
        except KeyError:
            raise serializers.ValidationError("Invalid sale_status value")

    def to_representation(self, instance):
        """
        Delegating response to custom made Response Serializer
        """
        return SalesResponseSerializer(context=self.context).to_representation(instance)

    def to_internal_value(self, data):
        """
        COnverting incoming human_readable data to corresponding database values
        """
        data = data.copy()  # making a mutable version of the data
        sale_status = data.pop("sale_status", None)
        transaction_type = data.pop("transaction_type", None)
        receipt_type = data.pop("receipt_type", None)
        if sale_status:
            data["sale_status"] = self.get_sale_status_db_value(sale_status)
        if transaction_type:
            data["transaction_type"] = self.get_transaction_type_db_value(transaction_type)
        if receipt_type:
            data["receipt_type"] = self.get_receipt_type_db_value(receipt_type)
        return super().to_internal_value(data)


class EmployeeSerializerAvecNameSole(serializers.ModelSerializer):
    """
    Serializer for Employee using the first and last names of user only
    """

    user = UserResponseSerializerAvecNameSole()

    class Meta:
        model = Employee
        fields = ["user"]


class CustomerSerializerAvecnameSole(serializers.ModelSerializer):
    """
    Serializer that just lists names only
    """

    class Meta:
        model = Customer
        fields = ["name"]


class SalesResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for Sales model
    """

    # business = BusinessSerializer(read_only=True)
    employee = EmployeeSerializerAvecNameSole()
    payment = PaymentModeResponseSerializer(read_only=True)
    customer = CustomerSerializerAvecnameSole(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    receipt_type = serializers.CharField(source="get_receipt_type_display", read_only=True)
    transaction_type = serializers.CharField(source="get_transaction_type_display", read_only=True)
    sale_status = serializers.CharField(source="get_sale_status_display", read_only=True)

    class Meta:
        model = Sales
        fields = [
            "uuid",
            "customer",
            "payment",
            "employee",
            "products",
            "sale_amount_with_tax",
            "tax_amount",
            "receipt_type",
            "transaction_type",
            "receipt_label",
            "sale_status",
            "amount_paid",
            "change",
            "created_at",
            "updated_at",
        ]


class SalesRelatedResponseSaleSerializer(serializers.ModelSerializer):
    """
    Serializer for related Sale model within ProductSales
    """

    # Customize the fields I want to include for the related Sale model
    class Meta:
        model = Sales
        fields = ["uuid", "created_at", "updated_at", "sale_status"]


class GenerateSaleReceiptSerializer(serializers.Serializer):
    """
    Serializer for request data to generate receipt and complete sale
    """

    payment_mode = serializers.CharField(required=True)
    amount_paid = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)


class GenerateSalesReportSerializer(serializers.Serializer):
    """
    Serializer for request data to generate sales summary report given start and end_date
    """

    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)


class GetProductSalesSerializer(serializers.Serializer):
    """
    Get the product_sales associted with a specific sale
    """


class ProductSalesSerializer(serializers.ModelSerializer):
    """
    Serializer for Request ProductSales model
    """

    product_uuid = serializers.UUIDField()
    sale_uuid = serializers.UUIDField()

    class Meta:
        model = ProductSales
        fields = [
            "uuid",
            "product_uuid",
            "sale_uuid",
            "quantity_sold",
            "price_per_unit",
            "is_wholesale",
            "price",
            "tax_amount",
            "tax_rate",
            "created_at",
            "updated_at",
        ]

    def validate(self, data):
        """
        Custome validate to map uuids to actual Related Objects
        """
        product_uuid = data.pop("product_uuid", None)
        sale_uuid = data.pop("sale_uuid", None)
        validated_data = super().validate(data)
        if product_uuid:
            product = get_object_or_404(Product, uuid=product_uuid)
            validated_data["product"] = product
        if sale_uuid:
            sale = get_object_or_404(Sales, uuid=sale_uuid)
            validated_data["sale"] = sale
        return validated_data

    def create(self, validated_data):
        """
        Overriding create method for adding business logic
        """
        # TODO: deal with discount arithmetic
        quantity_sold = validated_data.get("quantity_sold", "0")
        # discount = validated_data.get("discount", "0")
        stock = get_object_or_404(Stock, product_id=validated_data["product"].id)
        if Decimal(quantity_sold) > Decimal(stock.stock_quantity):
            validated_data["quantity_sold"] = stock.stock_quantity
        validated_data["price_per_unit"] = (
            stock.price_per_unit_wholesale if validated_data["is_wholesale"] else stock.price_per_unit_retail
        )
        validated_data["price"] = Decimal(quantity_sold) * Decimal(validated_data["price_per_unit"])
        # validated_data["price"] = Decimal(validated_data["price"]) - Decimal(discount)
        validated_data["tax_rate"] = validated_data["product"].tax_type
        total_amount = validated_data["product"].get_total_amount(
            Decimal(validated_data["price"]), validated_data["tax_rate"]
        )
        validated_data["tax_amount"] = (total_amount - Decimal(validated_data["price"])).quantize(
            Decimal("0.00"), rounding=ROUND_HALF_EVEN
        )
        sale = validated_data.get("sale", None)
        if sale:
            sale.sale_amount_with_tax += total_amount
            sale.tax_amount += validated_data["tax_amount"]
            sale.save()
        stock.update_stock_quantity(Stock.StockInOutType.Sale, quantity_sold, "Sale Made")
        return super().create(validated_data)

    def to_representation(self, instance):
        """
        Delegating response to another Serializer
        """
        return ProductSalesResponseSerializer(context=self.context).to_representation(instance)


class ProductSalesResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for Response ProductSales model
    """

    product = ProductSansSupplierResponseSerializer(read_only=True)
    sale = SalesRelatedResponseSaleSerializer(read_only=True)

    class Meta:
        model = ProductSales
        fields = [
            "uuid",
            "product",
            "sale",
            "quantity_sold",
            "price_per_unit",
            "is_wholesale",
            "price",
            "tax_amount",
            "tax_rate",
            "created_at",
            "updated_at",
        ]


class ProductSaleUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer tailor made for updating (partial or whole) of a ProductSale
    """

    quantity_sold = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    is_wholesale = serializers.BooleanField(required=True)

    class Meta:
        model = ProductSales
        fields = [
            "quantity_sold",
            "is_wholesale",
        ]

    def validate(self, data):
        """
        Validate the incoming update data
        """
        return super().validate(data)

    def update(self, instance, validated_data):
        """
        Custom logic for the update method of a productsale
        The update should only be limited to quantity_sold and
        is_wholesale, this is due to data integrity issues when
        updating the associated product and sale for this particular
        product_sold
        """

        quantity_sold = validated_data.get("quantity_sold", None)
        is_wholesale = validated_data.get("is_wholesale", None)
        with transaction.atomic():
            if quantity_sold:
                self.update_new_quantity_helper(instance, quantity_sold)
            if is_wholesale:
                self.update_new_wholesale_flag_helper(instance, is_wholesale)
        return super().update(instance, validated_data)

    def update_new_quantity_helper(self, product_sale, new_quantity_sold=None):
        """
        Helper function to update product_sales and dependecies
        when quantity changes
        """
        stock = get_object_or_404(Stock, product_id=product_sale.product.id)
        prev_quantity_sold = product_sale.quantity_sold
        stock.update_stock_quantity(Stock.StockInOutType.Return_in, prev_quantity_sold, "Sale Undone")
        stock.update_stock_quantity(Stock.StockInOutType.Sale, new_quantity_sold, "Sale Made")
        self.update_sale_amounts(product_sale, new_quantity_sold)

    def update_new_wholesale_flag_helper(self, product_sale, new_is_whole_sale):
        """
        helper function to update product_sale when a new whole-sale flag is passed in
        """
        stock = get_object_or_404(Stock, product_id=product_sale.product.id)
        product_sale.price_per_unit = (
            stock.price_per_unit_wholesale if new_is_whole_sale else stock.price_per_unit_retail
        )
        self.update_sale_amounts(product_sale, product_sale.quantity_sold)

    def update_sale_amounts(self, product_sale, quantity):
        """
        helper function to deal with sale amounts updating
        """
        previous_sold_amount_avec_tax = product_sale.product.get_total_amount(
            product_sale.price, product_sale.product.tax_type
        )
        product_sale.sale.sale_amount_with_tax -= previous_sold_amount_avec_tax
        product_sale.sale.tax_amount -= product_sale.tax_amount
        product_sale.quantity_sold = quantity
        new_price = Decimal(product_sale.price_per_unit) * Decimal(product_sale.quantity_sold)
        product_sale.price = new_price
        new_sold_amount_avec_tax = product_sale.product.get_total_amount(new_price, product_sale.product.tax_type)
        product_sale.tax_amount = new_sold_amount_avec_tax - new_price
        product_sale.sale.sale_amount_with_tax += new_sold_amount_avec_tax
        product_sale.sale.tax_amount += product_sale.tax_amount
        product_sale.sale.save()
        product_sale.save()

    def to_representation(self, instance):
        return ProductSalesResponseSerializer(context=self.context).to_representation(instance)


class PurchaseSerializer(serializers.ModelSerializer):
    """Serializer for Request Purchase"""

    employee_uuid = serializers.UUIDField(required=True)
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Purchase
        fields = [
            "uuid",
            "employee_uuid",
            "products",
            "created_at",
            "updated_at",
            "purchase_amount",
            "description",
        ]

    def validate(self, data):
        """Validate data by mapping uuids to ids required in database"""
        employee_uuid = data.pop("employee_uuid", None)
        validated_data = super().validate(data)
        if employee_uuid:
            employee = get_object_or_404(Employee, uuid=employee_uuid)
            validated_data["employee"] = employee
        return validated_data

    def to_representation(self, instance):
        return PurchaseResponseSerializer(context=self.context).to_representation(instance)


class PurchaseResponseSerializer(serializers.ModelSerializer):
    """Serializer for Response Purchase"""

    employee = EmployeeRestrictedSerializer(read_only=True)
    purchase_products = serializers.SerializerMethodField(method_name="get_purchase_products")

    class Meta:
        model = Purchase
        fields = [
            "uuid",
            "employee",
            "purchase_products",
            "created_at",
            "updated_at",
            "purchase_amount",
            "description",
        ]

    def get_purchase_products(self, obj: Any) -> list:
        """
        Get all purchase_products to highlight in purchases Response
        """
        from .serializers import PurchaseProductResponseSerializer

        purchase_products = obj.purchase_products.all()
        product_info = {}
        products = []
        for purchase_product in purchase_products:
            product_info["uuid"] = purchase_product.uuid
            product_info["product"] = purchase_product.product
            product_info["supplier"] = purchase_product.supplier
            product_info["product_quantity"] = purchase_product.product_quantity
            product_info["purchase_unit_price"] = purchase_product.purchase_unit_price
            product_info["total_product_cost"] = purchase_product.total_product_cost
            product_info["created_at"] = purchase_product.created_at
            product_info["updated_at"] = purchase_product.updated_at
            product_info["discount_applied"] = purchase_product.discount_applied
            product_info["description"] = purchase_product.description
            products.append(product_info)
            product_info = {}

        serializer = PurchaseProductResponseSerializer(products, many=True, partial=True)
        return serializer.data


class PurchaseRelatedResponseSerializer(serializers.ModelSerializer):
    """Serializer for without products Response for PurchaseProduct Viewset"""

    employee = EmployeeRestrictedSerializer(read_only=True)

    class Meta:
        model = Purchase
        fields = [
            "uuid",
            "employee",
            "created_at",
            "updated_at",
            "purchase_amount",
            "description",
        ]


class PurchaseProductResponseSerializer(serializers.ModelSerializer):
    """
    This is Response Serailizer for PurchaseProduct ViewSet
    """

    product = ProductSansSupplierResponseSerializer(read_only=True)
    purchase = PurchaseRelatedResponseSerializer(read_only=True)
    supplier = SupplierRelatedResponseSerializer(read_only=True)

    class Meta:
        model = PurchaseProduct
        fields = [
            "uuid",
            "product",
            "purchase",
            "supplier",
            "product_quantity",
            "purchase_unit_price",
            "total_product_cost",
            "created_at",
            "updated_at",
            "discount_applied",
            "description",
        ]


class PurchaseProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Request PurchaseStock ViewSet
    """

    product_uuid = serializers.UUIDField(required=True)
    purchase_uuid = serializers.UUIDField(required=True)
    supplier_uuid = serializers.UUIDField(required=True)

    class Meta:
        model = PurchaseProduct
        fields = [
            "uuid",
            "product_uuid",
            "purchase_uuid",
            "supplier_uuid",
            "product_quantity",
            "purchase_unit_price",
            "total_product_cost",
            "created_at",
            "updated_at",
            "discount_applied",
            "description",
        ]

    def validate(self, data):
        """Validate the data by mapping product and purchase uuids to"""
        product_uuid = data.pop("product_uuid", None)
        purchase_uuid = data.pop("purchase_uuid", None)
        supplier_uuid = data.pop("supplier_uuid", None)
        validated_data = super().validate(data)
        if product_uuid:
            product = get_object_or_404(Product, uuid=product_uuid)
            validated_data["product"] = product
        if purchase_uuid:
            purchase = get_object_or_404(Purchase, uuid=purchase_uuid)
            validated_data["purchase"] = purchase
        if supplier_uuid:
            supplier = get_object_or_404(Supplier, uuid=supplier_uuid)
            validated_data["supplier"] = supplier
        return validated_data

    def create(self, validated_data):
        """
        Overriding create method for handling extra business logic
        """
        quantity = validated_data.get("product_quantity", "0")
        unit_price = validated_data.get("purchase_unit_price", "0")
        validated_data["total_product_cost"] = Decimal(quantity) * Decimal(unit_price)
        purchase = validated_data.get("purchase", None)
        if purchase:
            purchase.purchase_amount += validated_data["total_product_cost"]
            purchase.save()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Custom validation for update
        """
        quantity = validated_data.get("product_quantity", instance.product_quantity)
        unit_price = validated_data.get("purchase_unit_price", instance.purchase_unit_price)
        purchase = validated_data.get("purchase", instance.purchase)
        validated_data["total_product_cost"] = Decimal(quantity) * Decimal(unit_price)
        purchase.purchase_amount -= instance.total_product_cost
        purchase.purchase_amount += validated_data["total_product_cost"]
        purchase.save()
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        return PurchaseProductResponseSerializer(context=self.context).to_representation(instance)


class SalesNotFoundSerializer(serializers.Serializer):
    detail = serializers.CharField(default="Unfortunately requested resource not found")
