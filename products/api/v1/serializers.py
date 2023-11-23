"""
Module for creating serializers for Product application models
"""
from typing import Any
from django.db.models import Q
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from products.models import Category, Product, Stock, SupplierProduct, StockMovement
from administration.models import Employee, Supplier
from administration.api.v1.serializers import EmployeeRestrictedSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model
    """

    class Meta:
        model = Category
        fields = ["name", "uuid", "image", "thumbnail", "created_at", "updated_at"]


class CategoryResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for Response of the Category
    """

    class Meta:
        fields = ["name", "thumbnail"]


class SupplierRelatedResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for Supplier response embedded in other serializers
    """

    class Meta:
        model = Supplier
        fields = [
            "uuid",
            "name",
            "address",
            "email_address",
            "phone_number",
            "created_at",
            "updated_at",
        ]


class ProductListSuppliersSerializer(serializers.Serializer):
    """
    Custom serializer to include leadtime
    """

    uuid = serializers.UUIDField()
    name = serializers.CharField()
    address = serializers.CharField()
    email_address = serializers.EmailField()
    phone_number = serializers.CharField()
    lead_time = serializers.DecimalField(max_digits=5, decimal_places=2)


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Product model Request data
    """

    category = serializers.UUIDField(read_only=True)
    suppliers = SupplierRelatedResponseSerializer(many=True, read_only=True)
    packaging_unit = serializers.CharField(required=False)
    unit = serializers.CharField(required=False)
    product_type = serializers.CharField(required=False)
    tax_type = serializers.CharField(required=False)

    class Meta:
        model = Product
        fields = [
            "uuid",
            "category",
            "name",
            "suppliers",
            "code",
            "description",
            "product_type",
            "tax_type",
            "unit",
            "limited",
            "active_for_sale",
            "created_at",
            "updated_at",
            "packaging_unit",
        ]

    # Converting to database values from Human-readable/friendly values in the request data

    def get_packaging_unit_db_value(self, human_readable_value):
        """
        Get Database value from human_readable value
        """
        packaging_unit_choices = Product.PackagingUnit.choices
        try:
            packaging_unit_choices_dict = dict((y, x) for x, y in packaging_unit_choices)
            return packaging_unit_choices_dict[human_readable_value]
        except KeyError:
            raise serializers.ValidationError("Invalid tax_type value.")

    def get_unit_db_value(self, human_readable_value):
        """
        Get Database value from human_readable value
        """
        unit_choices = Product.UnitOfQuantity.choices
        try:
            unit_choices_dict = dict((y, x) for x, y in unit_choices)
            return unit_choices_dict[human_readable_value]
        except KeyError:
            raise serializers.ValidationError("Invalid tax_type value.")

    def get_tax_type_db_value(self, human_readable_value):
        """
        Get Database value from human_readable value
        """
        tax_type_choices = Product.TaxType.choices
        try:
            tax_type_choices_dict = dict((y, x) for x, y in tax_type_choices)
            return tax_type_choices_dict[human_readable_value]
        except KeyError:
            raise serializers.ValidationError("Invalid tax_type value.")

    def get_product_type_db_value(self, human_readable_value):
        """
        Get Database value from human_readable value
        """
        product_type_choices = Product.ProductType.choices
        try:
            product_type_choices_dict = dict((y, x) for x, y in product_type_choices)
            return product_type_choices_dict[human_readable_value]
        except KeyError:
            raise serializers.ValidationError("Invalid tax_type value.")

    def validate(self, data):
        """
        Custom validation due to the Enum fields
        """
        category_uuid = data.pop("category", None)
        validated_data = super().validate(data)
        if category_uuid:
            category = get_object_or_404(Category, uuid=category_uuid)
            validated_data["category"] = category
        return validated_data

    def to_representation(self, instance):
        """
        Delegating response data to appropriate ProductResponseSerializer
        """
        return ProductResponseSerializer(context=self.context).to_representation(instance)

    def to_internal_value(self, data):
        """
        Validate and return to database value during deserialization
        """
        data = data.copy()
        packaging_unit = data.pop("packaging_unit", None)
        product_type = data.pop("product_type", None)
        tax_type = data.pop("tax_type", None)
        unit = data.pop("unit", None)
        if packaging_unit:
            data["packaging_unit"] = self.get_packaging_unit_db_value(packaging_unit)
        if product_type:
            data["product_type"] = self.get_product_type_db_value(product_type)
        if tax_type:
            data["tax_type"] = self.get_tax_type_db_value(tax_type)
        if unit:
            data["unit"] = self.get_unit_db_value(unit)
        return super().to_internal_value(data)


class ProductResponseSerializer(serializers.ModelSerializer):
    """
    Product Serializer for Response data
    """

    category = CategorySerializer()
    suppliers = SupplierRelatedResponseSerializer(many=True, read_only=True)
    packaging_unit = serializers.CharField(source="get_packaging_unit_display", read_only=True)
    unit = serializers.CharField(source="get_unit_display", read_only=True)
    product_type = serializers.CharField(source="get_product_type_display", read_only=True)
    tax_type = serializers.CharField(source="get_tax_type_display", read_only=True)

    class Meta:
        model = Product
        fields = [
            "uuid",
            "category",
            "name",
            "suppliers",
            "code",
            "description",
            "product_type",
            "tax_type",
            "unit",
            "limited",
            "active_for_sale",
            "created_at",
            "updated_at",
            "packaging_unit",
        ]


class SupplierListAllProductsSerializer(serializers.Serializer):
    """
    Serializer to list all products associated with a supplier
    """

    category = serializers.CharField()
    name = serializers.CharField()
    uuid = serializers.UUIDField()
    code = serializers.CharField()
    description = serializers.CharField()
    product_type = serializers.CharField()
    tax_type = serializers.CharField()
    packaging_unit = serializers.CharField()
    unit = serializers.CharField()
    limited = serializers.BooleanField()
    active_for_sale = serializers.BooleanField()


class ProductSansSupplierResponseSerializer(serializers.ModelSerializer):
    """
    Product Serializer for Response data without supplier data to
    be embedded in other serializers
    """

    category = serializers.UUIDField()
    packaging_unit = serializers.CharField(source="get_packaging_unit_display", read_only=True)
    unit = serializers.CharField(source="get_unit_display", read_only=True)
    product_type = serializers.CharField(source="get_product_type_display", read_only=True)
    tax_type = serializers.CharField(source="get_tax_type_display", read_only=True)

    class Meta:
        model = Product
        fields = [
            "uuid",
            "category",
            "name",
            "code",
            "description",
            "product_type",
            "tax_type",
            "unit",
            "limited",
            "active_for_sale",
            "created_at",
            "updated_at",
            "packaging_unit",
        ]


class ProductSearchSerializer(serializers.Serializer):
    """
    Custom serializer for search request query
    """

    query = serializers.CharField()

    def search_products(self):
        """
        Perform search functionality on the products
        using name/code/description
        """
        query = self.validated_data.get("query", "")
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query) | Q(code__icontains=query)
            )
            serializer = ProductResponseSerializer(products, many=True)
            return serializer.data
        return []


class CategorySearchSerializer(serializers.Serializer):
    """
    Custom serializer for search request query
    """

    query = serializers.CharField()

    def search_category(self):
        """
        Perform search functionality on the caegories
        using name/code/description
        """
        query = self.validated_data.get("query", "")
        if query:
            categories = Category.objects.filter(Q(name__icontains=query) | Q(uuid__icontains=query))
            serializer = CategorySerializer(categories, many=True)
            return serializer.data
        return []


class SupplierSerializer(serializers.ModelSerializer):
    """
    Serializer for Request Supplier model
    """

    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Supplier
        fields = [
            "uuid",
            "products",
            "name",
            "address",
            "email_address",
            "phone_number",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        """
        Delegating the response supplier data to appropriate serializer
        """
        return SupplierResponseSerializer(context=self.context).to_representation(instance)


class SupplierResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for Response Supplier Object
    """

    products = ProductSansSupplierResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Supplier
        fields = [
            "uuid",
            "products",
            "name",
            "address",
            "email_address",
            "phone_number",
            "created_at",
            "updated_at",
        ]


class SupplierProductSerializer(serializers.ModelSerializer):
    """
    Serializer for Request data for the SupplierProduct Object
    """

    supplier_uuid = serializers.UUIDField(required=True)
    product_uuid = serializers.UUIDField(required=True)
    lead_time = serializers.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        model = SupplierProduct
        fields = ["uuid", "supplier_uuid", "product_uuid", "lead_time"]

    def validate(self, data):
        """
        Custome validation mapping uuids to respective objects
        """
        supplier_uuid = data.pop("supplier_uuid", None)
        product_uuid = data.pop("product_uuid", None)
        validated_data = super().validate(data)
        if supplier_uuid:
            supplier = get_object_or_404(Supplier, uuid=supplier_uuid)
            validated_data["supplier"] = supplier
        if product_uuid:
            product = get_object_or_404(Product, uuid=product_uuid)
            validated_data["product"] = product
        return validated_data

    def create(self, validated_data):
        """
        Create method for custom serailizer required
        """
        return super().create(validated_data)

    def to_representation(self, instance):
        """
        Delegating response to appropriate Serializer
        """
        return SupplierProductResponseSerializer(context=self.context).to_representation(instance)


class SupplierProductResponseSerializer(serializers.ModelSerializer):
    """
    Supplier for Response Object of SupplierProduct Objects
    """

    supplier = SupplierRelatedResponseSerializer(read_only=True)
    product = ProductSansSupplierResponseSerializer(read_only=True)

    class Meta:
        model = SupplierProduct
        fields = ["uuid", "supplier", "product", "lead_time"]


class StockSerializer(serializers.ModelSerializer):
    """
    Serializer for Stock model
    """

    # Use the ProductSerializer as a nested serializer for the product_id field
    # if the relationship between Product and Stock is frequently accessed together,
    # embedding could be more beneficial.
    # If not, using the foreign key and making separate calls might be more efficient.
    # Should monitor this to get the correct way of embeddding or just haveing the foreignkey
    product_uuid = serializers.UUIDField()

    class Meta:
        model = Stock
        fields = [
            "uuid",
            "product_uuid",
            "stock_quantity",
            "created_at",
            "updated_at",
            "cost_per_unit",
            "price_per_unit_retail",
            "price_per_unit_wholesale",
            "reorder_level",
            "reorder_quantity",
            "latest_stock_movement_type",
            "latest_stock_movement_quantity",
            "latest_stock_movement_remarks",
        ]

    def validate(self, data):
        """
        Custom validation mapping product_uuid to product
        """
        product_uuid = data.pop("product_uuid", None)

        validated_data = super().validate(data)
        if product_uuid:
            product = get_object_or_404(Product, uuid=product_uuid)
            validated_data["product"] = product
        return validated_data

    def create(self, validated_data):
        """
        Custom creation logic to take care of StockMovement
        """
        stock = Stock(**validated_data)
        stock.save()
        StockMovement.objects.create(
            stock=stock,
            movement_type=validated_data.get("latest_stock_movement_type"),
            movement_quantity=validated_data.get("latest_stock_movement_quantity"),
            remarks=validated_data.get("latest_stock_movement_remarks"),
            previous_stock_quantity=stock.stock_quantity,
        )
        return stock

    def update(self, instance, validated_data):
        """
        update stock quantities accordingly
        """
        instance.update_stock_quantity(
            validated_data.get("latest_stock_movement_type"),
            validated_data.get("latest_stock_movement_quantity"),
            validated_data.get("latest_stock_movement_remarks"),
        )
        return super().update(instance, validated_data)

    def get_latest_stock_movement_type_db_value(self, human_readable_val):
        """
        Get the database version of latest_stock_movement_type
        """
        latest_stock_movement_type_choices = Stock.StockInOutType.choices
        try:
            latest_stock_movement_type_dict = dict((y, x) for (x, y) in latest_stock_movement_type_choices)
            return latest_stock_movement_type_dict[human_readable_val]
        except KeyError:
            raise serializers.ValidationError("Invalid latest_stock_movement_type value.")

    def to_representation(self, instance):
        """
        Delegating response data to appropriate Response Object Serializer
        """
        return StockResponseSerializer(context=self.context).to_representation(instance)

    def to_internal_value(self, data):
        """
        Change stock_movement_type to database value
        """
        data = data.copy()
        latest_stock_movement_type = data.pop("latest_stock_movement_type", None)
        if latest_stock_movement_type:
            data["latest_stock_movement_type"] = self.get_latest_stock_movement_type_db_value(
                latest_stock_movement_type
            )
        return super().to_internal_value(data)


class StockResponseSerializer(serializers.ModelSerializer):
    """
    Serializer for stock object Response
    """

    latest_stock_movement_type = serializers.CharField(source="get_latest_stock_movement_type_display", read_only=True)
    product = ProductResponseSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = [
            "uuid",
            "product",
            "stock_quantity",
            "created_at",
            "updated_at",
            "cost_per_unit",
            "price_per_unit_retail",
            "price_per_unit_wholesale",
            "reorder_level",
            "reorder_quantity",
            "latest_stock_movement_type",
            "latest_stock_movement_quantity",
            "latest_stock_movement_remarks",
        ]


class GenerateStockMovementReportSerializer(serializers.Serializer):
    """
    Serializer for request data to generate Stock Movement of a particular stock
    summary report given start and end_date
    """

    start_date = serializers.DateField(required=True)
    end_date = serializers.DateField(required=True)


class StockSearchSerializer(serializers.Serializer):
    """
    Custom serializer for search request query
    """

    query = serializers.CharField()

    def search_stock(self):
        """
        Perform search functionality on the stocks using
        using product name/code/description
        """
        query = self.validated_data.get("query", "")
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query) | Q(code__icontains=query)
            )
            stocks = Stock.objects.filter(product__in=products)
            serializer = StockSerializer(stocks, many=True)
            return serializer.data
        return []


class StockMovementSerializer(serializers.ModelSerializer):
    """
    Serializer for StockMovement Request data
    """

    stock_uuid = serializers.UUIDField()
    employee_uuid = serializers.UUIDField()

    class Meta:
        model = StockMovement
        fields = [
            "uuid",
            "stock_uuid",
            "movement_type",
            "movement_quantity",
            "remarks",
            "created_at",
            "previous_stock_quantity",
            "employee_uuid",
        ]

    def validate(self, data):
        """
        Custom validation mapping stock_uuid to stock and
        employee_uuid to employee
        """
        stock_uuid = data.pop("stock_uuid", None)
        employee_uuid = data.pop("employee_uuid", None)
        validated_data = super().validate(data)
        if stock_uuid:
            stock = get_object_or_404(Stock, uuid=stock_uuid)
            validated_data["stock"] = stock
        if employee_uuid:
            employee = get_object_or_404(Employee, uuid=employee_uuid)
        return validated_data

    def create(self, validated_data):
        """Custom logic for creation since this affects the stock model"""
        stock = validated_data.get("stock", None)
        if stock:
            stock_movement = stock.update_stock_quantity(
                validated_data["movement_type"], validated_data["movement_quantity"], validated_data["remarks"]
            )
            return stock_movement

    def update(self, instance, validated_data):
        """
        Custom logic for updating the stock accurately
        """
        stock = validated_data.get("stock", None)
        if not stock:
            stock = instance.stock
        stock_movement = stock.update_stock_quantity(
            validated_data["movement_type"], validated_data["movement_quantity"], validated_data["remarks"]
        )
        return stock_movement

    def get_movement_type_db_value(self, human_readable_val):
        """
        Get the database version of latest_stock_movement_type
        """
        movement_type_choices = Stock.StockInOutType.choices
        try:
            movement_type_dict = dict((y, x) for (x, y) in movement_type_choices)
            return movement_type_dict[human_readable_val]
        except KeyError:
            raise serializers.ValidationError("Invalid movement_type value.")

    def to_representation(self, instance):
        """
        Delegatig the Response data to appropriate Response
        Serializer
        """
        return StockMovementResponseSerializer(context=self.context).to_representation(instance)

    def to_internal_value(self, data):
        """
        Change stock_movement_type to database value
        """
        data = data.copy()
        movement_type = data.pop("movement_type", None)
        if movement_type:
            data["movement_type"] = self.get_movement_type_db_value(movement_type)
        return super().to_internal_value(data)


class StockMovementResponseSerializer(serializers.ModelSerializer):
    """
    Serialier for StockMovement Response data
    """

    movement_type = serializers.CharField(source="get_movement_type_display", read_only=True)
    stock = StockResponseSerializer(read_only=True)
    employee = EmployeeRestrictedSerializer()

    class Meta:
        model = StockMovement
        fields = [
            "uuid",
            "stock",
            "movement_type",
            "movement_quantity",
            "remarks",
            "created_at",
            "previous_stock_quantity",
            "employee",
        ]


class ProductSerializerAvecNameSole(serializers.ModelSerializer):
    """
    Custom Serializer that just contains a product name only
    for nesting purposes
    """

    class Meta:
        model = Product
        fields = ["name"]


class StockMovementSansStockResponseSerializer(serializers.ModelSerializer):
    """
    Serialier for StockMovement Response data
    """

    movement_type = serializers.CharField(source="get_movement_type_display", read_only=True)

    class Meta:
        model = StockMovement
        fields = [
            "uuid",
            "movement_type",
            "movement_quantity",
            "remarks",
            "created_at",
            "previous_stock_quantity",
            "employee",
        ]


class StockMovementAvecProductSerializer(serializers.Serializer):
    """
    Custom Serializer for StockMovement Requests data in generate
    list_all_stock_movements in Stocks ViewSet
    """


class StockMovementAvecProductResponseSerializer(serializers.ModelSerializer):
    """
    Custom Serializer for StockMovement Response data in generate
    list_all_stock_movements in Stocks ViewSet
    """

    product = ProductSerializerAvecNameSole()
    stock_movement = StockMovementSansStockResponseSerializer()

    class Meta:
        model = StockMovement
        fields = ["product", "stock_movement"]


class ProductListStockSerializer(serializers.ModelSerializer):
    """
    Serializer to be used to list Stock associated with
    a product
    """

    product_name = serializers.SerializerMethodField(method_name="get_product_name")
    product_code = serializers.SerializerMethodField(method_name="get_product_code")

    class Meta:
        model = Stock
        fields = [
            "uuid",
            "stock_quantity",
            "created_at",
            "updated_at",
            "cost_per_unit",
            "price_per_unit_retail",
            "price_per_unit_wholesale",
            "reorder_level",
            "reorder_quantity",
            "latest_stock_movement_type",
            "latest_stock_movement_quantity",
            "latest_stock_movement_remarks",
            "product_name",
            "product_code",
        ]

    def get_product_name(self, obj) -> str:
        """
        Get name of stock product object
        """
        return obj.product.name

    def get_product_code(self, obj) -> str:
        """
        Get code of stock product object
        """
        return obj.product.code


class ProductNotFoundSerializer(serializers.Serializer):
    detail = serializers.CharField(default="Unfortunately requested resource not found")
