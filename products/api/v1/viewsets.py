"""
Module illustrating the viewsets for product API's
"""
from datetime import datetime
from administration.models import Supplier
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from products.models import Product, Category, Stock, SupplierProduct
from sales.models import Sales
from .serializers import (
    ProductSerializer,
    CategorySerializer,
    StockSerializer,
    SupplierSerializer,
    SupplierProductSerializer,
)


class CategoryViewSet(ViewSet):
    """Basic viewset for Category Related Items"""

    serializer_class = CategorySerializer
    lookup_field = "uuid"

    @property
    def queryset(self):
        return Category.objects.all()

    def list(self, request, *args, **kwargs):
        """Return a list of all categories"""
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Category.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, uuid=None):
        """Return a single category"""
        category = get_object_or_404(self.queryset, uuid=uuid)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new category"""
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Category.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, uuid=None):
        """Update an existing category"""
        category = get_object_or_404(self.queryset, uuid=uuid)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Category.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, uuid=None):
        """Update an existing category"""
        category = get_object_or_404(self.queryset, uuid=uuid)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Category.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, uuid=None):
        """Delete an existing category"""
        category = get_object_or_404(self.queryset, uuid=uuid)
        category.delete()
        return Response(status=204)

    @action(detail=False, methods=["POST"])
    def search(self, request, *args, **kwargs):
        query = request.data.get("query", "")
        if query:
            categories = Category.objects.filter(
                Q(name__icontains=query) | Q(uuid__icontains=query)
            )
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)
        return Response({"categories": []})

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Category.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    @action(detail=True, methods=["GET"])
    def list_all_products(self, request, uuid=None):
        """List all products in a category"""
        category = get_object_or_404(self.queryset, uuid=uuid)
        products = category.products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductViewSet(ViewSet):
    """Basic viewset for Product Related Items"""

    serializer_class = ProductSerializer
    lookup_field = "uuid"

    @property
    def product_queryset(self):
        return Product.objects.all()

    @property
    def category_queryset(self):
        return Category.objects.all()

    def list(self, request, *args, **kwargs):
        """Return a list of all products"""
        serializer = ProductSerializer(self.product_queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Product.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, uuid=None):
        """Return a single product"""
        product = get_object_or_404(self.product_queryset, uuid=uuid)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new product"""
        data = request.data
        uuid = data.get("category", None)
        if uuid:
            category = get_object_or_404(self.category_queryset, uuid=uuid)
            data["category"] = category.id
            serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Product.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, uuid=None):
        """Update an existing product"""
        product = get_object_or_404(self.product_queryset, uuid=uuid)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Product.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, uuid=None):
        """Update an existing product"""
        product = get_object_or_404(self.product_queryset, uuid=uuid)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Product.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, uuid=None):
        """Delete an existing product"""
        product = get_object_or_404(self.product_queryset, uuid=uuid)
        product.delete()
        return Response(status=204)

    @action(detail=False, methods=["POST"])
    def search(self, request, *args, **kwargs):
        """
        Searches and enumerates possible products matching query
        """
        query = request.data.get("query", "")
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query)
                | Q(description__icontains=query)
                | Q(code__icontains=query)
            )
            serializer = ProductSerializer(products, many=True)
            return Response(serializer.data)
        return Response({"products": []})


class StockViewSet(ViewSet):
    """ViewSet for Stock  Items"""

    serializer_class = StockSerializer
    lookup_field = "uuid"

    @property
    def stock_queryset(self):
        return Stock.objects.all()

    @property
    def product_queryset(self):
        return Product.objects.all()

    def list(self, request, *args, **kwargs):
        """Return a list of all stock"""
        serializer = StockSerializer(self.stock_queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Stock item.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, uuid=None):
        """Return a single stock"""
        stock = get_object_or_404(self.stock_queryset, uuid=uuid)
        serializer = StockSerializer(stock)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new stock"""
        data = request.data
        uuid = data.get("product_id", None)
        if uuid:
            product = get_object_or_404(self.product_queryset, uuid=uuid)
            data["product_id"] = product.id
            serializer = StockSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Stock item.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, uuid=None):
        """Update an existing stock"""
        stock = get_object_or_404(self.stock_queryset, uuid=uuid)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Stock item.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, uuid=None):
        """Update an existing stock"""
        stock = get_object_or_404(self.stock_queryset, uuid=uuid)
        serializer = StockSerializer(stock, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Stock item.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, uuid=None):
        """Delete an existing stock"""
        stock = get_object_or_404(self.stock_queryset, uuid=uuid)
        stock.delete()
        return Response(status=204)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Stock item.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    @action(detail=True, methods=["POST"])
    def stock_movement(self, request, uuid=None):
        """Method that updates stock according to the typr of movement"""
        stock = get_object_or_404(self.stock_queryset, uuid=uuid)

        stock_movement_type = request.data.get("stock_movement_type")
        stock_movement_quantity = request.data.get("stock_movement_quantity")
        stock_movement_remarks = request.data.get("stock_movement_remarks")
        print(request.data)
        if stock_movement_type:
            stock.update_stock_quantity(
                stock_movement_type, stock_movement_quantity, stock_movement_remarks
            )
            serializer = StockSerializer(stock, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        return Response({"error": "No stock movement type given"}, status=400)

    @action(detail=False, methods=["POST"])
    def generate_stock_movement_report(self, request, pk=None):
        """
        Generate stock movement report for a given date range
        """
        data = request.data
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)
        if start_date and end_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            return Response(
                {"message": "Please provide a start date and end date"},
                status=400,
            )

        # Filter stock items based on the date range
        stocks = Stock.objects.filter(updated_at__date__range=[start_date, end_date])

        if not stocks:
            return Response(
                {"message": "No stock movement found for the given date range"},
                status=400,
            )

        report = {
            "start_date": start_date,
            "end_date": end_date,
            "stock_movement": [],
        }

        for stock in stocks:
            stock_movement = {
                "stock_id": stock.uuid,
                "product_name": stock.product_id.name,
                "stock_quantity": stock.stock_quantity,
                "stock_updated_at": stock.updated_at,
                "cost_per_unit": stock.cost_per_unit,
                "price_per_unit_retail": stock.price_per_unit_retail,
                "price_per_unit_wholesale": stock.price_per_unit_wholesale,
                "reorder_level": stock.reorder_level,
                "reorder_quantity": stock.reorder_quantity,
                "stock_movement_type": stock.stock_movement_type,
                "stock_movement_quantity": stock.stock_movement_quantity,
                "stock_movement_remarks": stock.stock_movement_remarks,
            }
            report["stock_movement"].append(stock_movement)

        return Response(
            {"stock_movement_report": report},
            status=200,
        )

    @action(detail=False, methods=["POST"])
    def search(self, request, *args, **kwargs):
        """
        Returns stock information for product name, description or code  in query
        """
        query = request.data.get("query", "")
        product = Product.objects.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(code__icontains=query)
        ).first()
        if query:
            stock = Stock.objects.get(pk=product.id)
            serializer = StockSerializer(stock)
            return Response(serializer.data)
        return Response({"stocks": []})


class SupplierProductViewSet(ViewSet):
    """
    API endpoint that allows suppliers to be viewed or edited.
    """

    serializer_class = SupplierProductSerializer
    lookup_field = "uuid"

    @property
    def supplier_queryset(self):
        return Sales.objects.all()

    @property
    def product_queryset(self):
        return Product.objects.all()

    @property
    def supplier_product_queryset(self):
        return SupplierProduct.objects.all()

    def list(self, request, *args, **kwargs):
        """
        List all supplier products
        """
        serializer = SupplierProductSerializer(
            self.supplier_product_queryset, many=True
        )
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this SupplierProduct.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, uuid=None):
        """
        Retun a single SupplierProduct
        """
        product_sale = get_object_or_404(self.supplier_product_queryset, uuid=uuid)
        serializer = SupplierProductSerializer(product_sale)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new SupplierProduct"""
        serializer = SupplierProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this SupplierProduct.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, uuid=None):
        """Update a SupplierProduct"""
        product_sale = get_object_or_404(self.supplier_product_queryset, uuid=uuid)
        serializer = SupplierProductSerializer(product_sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this SupplierProduct.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, uuid=None):
        """Update a SupplierProduct"""
        product_sale = get_object_or_404(self.supplier_product_queryset, uuid=uuid)
        serializer = SupplierProductSerializer(
            product_sale, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this SupplierProduct.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, uuid=None):
        """Delete a SupplierProduct"""
        product_sale = get_object_or_404(self.supplier_product_queryset, uuid=uuid)
        product_sale.delete()
        return Response(status=204)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Supplier.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    @action(detail=False, methods=["GET"])
    def list_all_supplier_products(self, request, uuid=None):
        """
        List all SupplierProducts for a Supplier
        """
        supplier = get_object_or_404(self.supplier_queryset, uuid=uuid)
        supplier_products = get_list_or_404(
            self.supplier_product_queryset, supplier=supplier.id
        )
        serializer = SupplierProductSerializer(supplier_products, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Product.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    @action(detail=False, methods=["GET"])
    def list_all_product_supplier(self, request, uuid=None):
        """
        List all Suppliers associated with a Product
        """
        product = get_object_or_404(self.product_queryset, uuid=uuid)
        product_supplier = get_list_or_404(
            self.supplier_product_queryset, product=product.id
        )
        serializer = SupplierProductSerializer(product_supplier, many=True)
        return Response(serializer.data)


class SupplierViewSet(ViewSet):
    """API endpoit that allows Suppliers to be viewed and edited"""

    serializer_class = SupplierSerializer
    lookup_field = "uuid"

    @property
    def supplier_queryset(self):
        return Supplier.objects.all()

    @property
    def product_queryset(self):
        return Product.objects.all()

    def list(self, request, *args, **kwargs):
        """Return a list of all suppliers"""
        serializer = SupplierSerializer(self.supplier_queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Supplier.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, uuid=None):
        """Return a single supplier"""
        supplier = get_object_or_404(self.supplier_queryset, uuid=uuid)
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new supplier"""
        print(request.data)
        data = request.data
        product_uuids = data.pop("products")
        print(product_uuids)
        product_ids = []
        for uuid in product_uuids:
            product = get_object_or_404(self.product_queryset, uuid=uuid)
            print(uuid, product)
            product_ids.append(product.id)
        print(product_ids)
        data["products"] = product_ids
        serializer = SupplierSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Supplier.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, uuid=None):
        """Update an existing supplier"""
        supplier = get_object_or_404(self.supplier_queryset, uuid=uuid)
        serializer = SupplierSerializer(supplier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Supplier.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, uuid=None):
        """Update an existing supplier partially"""
        supplier = get_object_or_404(self.supplier_queryset, uuid=uuid)
        serializer = SupplierSerializer(supplier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Supplier.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, uuid=None):
        """Delete an existing supplier"""
        supplier = get_object_or_404(self.supplier_queryset, uuid=uuid)
        supplier.delete()
        return Response(status=204)
