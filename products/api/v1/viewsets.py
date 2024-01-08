"""
Module illustrating the viewsets for product API's
"""
from datetime import datetime
from pos_inventory.utils.decorators import response_schema
from administration.models import Supplier
from django.utils.timezone import make_aware
from django.shortcuts import get_object_or_404, get_list_or_404
from django.db.models import Q

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from products.models import Product, Category, Stock, SupplierProduct, StockMovement
from sales.models import Sales, ProductSales, PurchaseProduct, PaymentMode
from sales.api.v1.serializers import (
    CustomerSerializer,
    EmployeeRestrictedSerializer,
    PaymentModeSerializer,
    SalesResponseSerializer,
)
from administration.api.v1.serializers import (
    EmployeeSerializer,
)
from .serializers import (
    ProductSerializer,
    ProductResponseSerializer,
    ProductListSuppliersSerializer,
    ProductSearchSerializer,
    ProductListStockSerializer,
    ProductSansSupplierResponseSerializer,
    ProductNotFoundSerializer,
    CategorySerializer,
    CategorySearchSerializer,
    StockSerializer,
    StockResponseSerializer,
    StockMovementSerializer,
    StockMovementResponseSerializer,
    GenerateStockMovementReportSerializer,
    StockMovementSansStockResponseSerializer,
    StockSearchSerializer,
    StockMovementAvecProductSerializer,
    StockMovementAvecProductResponseSerializer,
    SupplierSerializer,
    SupplierProductSerializer,
    SupplierProductResponseSerializer,
    SupplierResponseSerializer,
    SupplierListAllProductsSerializer,
    SupplierRelatedResponseSerializer,
)


class CategoryViewSet(ViewSet):
    """Basic viewset for Category Related Items"""

    # permission_classes = (CategoryAccessPolicy,)
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
        responses={
            status.HTTP_404_NOT_FOUND: ProductNotFoundSerializer,
        },
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
        responses={
            status.HTTP_404_NOT_FOUND: ProductNotFoundSerializer,
        },
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
        responses={
            status.HTTP_404_NOT_FOUND: ProductNotFoundSerializer,
        },
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
        responses={
            status.HTTP_404_NOT_FOUND: ProductNotFoundSerializer,
        },
    )
    def destroy(self, request, uuid=None):
        """Delete an existing category"""
        category = get_object_or_404(self.queryset, uuid=uuid)
        category.delete()
        return Response(status=204)

    @extend_schema(
        request=CategorySearchSerializer,
        responses={
            status.HTTP_200_OK: CategorySerializer(many=True),
            status.HTTP_404_NOT_FOUND: ProductNotFoundSerializer,
        },
    )
    @action(detail=False, methods=["POST"])
    def search(self, request, *args, **kwargs):
        serializer = CategorySearchSerializer(data=request.data)
        if serializer.is_valid():
            categories = serializer.search_category()
            return Response(categories, status=200)
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
        responses={
            status.HTTP_200_OK: ProductSansSupplierResponseSerializer(many=True),
            status.HTTP_404_NOT_FOUND: ProductNotFoundSerializer,
        },
    )
    @action(detail=True, methods=["GET"])
    def list_all_products(self, request, uuid=None):
        """List all products in a category"""
        category = get_object_or_404(self.queryset, uuid=uuid)
        products = category.products.all()
        serializer = ProductSansSupplierResponseSerializer(products, many=True)
        return Response(serializer.data)


@response_schema(serializer=ProductSansSupplierResponseSerializer)
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
        serializer = ProductSerializer(data=request.data)
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
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=204)

    @extend_schema(
        description="Retrieves a list of suppliers for a particular Product.",
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Product.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            status.HTTP_200_OK: ProductListSuppliersSerializer(many=True),
            status.HTTP_404_NOT_FOUND: ProductNotFoundSerializer,
        },
    )
    @action(detail=True, methods=["get"])
    def list_suppliers(self, request, uuid=None):
        """List all suppliers of a product"""
        product = get_object_or_404(self.product_queryset, uuid=uuid)
        product_suppliers = product.supplierproduct_set.all()
        suppliers_data = [
            {
                "uuid": supplier_product.supplier.uuid,
                "name": supplier_product.supplier.name,
                "address": supplier_product.supplier.address,
                "email_address": supplier_product.supplier.email_address,
                "phone_number": supplier_product.supplier.phone_number,
                "lead_time": supplier_product.lead_time,
            }
            for supplier_product in product_suppliers
        ]
        serializer = ProductListSuppliersSerializer(data=suppliers_data, many=True)
        if serializer.is_valid():
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    @extend_schema(
        description="Retrieves a list of Products according to query.",
        request=ProductSearchSerializer,
        responses={
            status.HTTP_200_OK: ProductSerializer(many=True),
        },
    )
    @action(detail=False, methods=["POST"])
    def search(self, request, *args, **kwargs):
        """
        Searches and enumerates possible products matching query
        """
        serializer = ProductSearchSerializer(data=request.data)
        if serializer.is_valid():
            search_results = serializer.search_products()
            return Response(search_results, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        description="Retrieves a Stock Information for a particular Product.",
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Product.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            status.HTTP_200_OK: ProductListStockSerializer(),
            status.HTTP_404_NOT_FOUND: ProductNotFoundSerializer,
        },
    )
    @action(detail=True, methods=["GET"])
    def stock_information(self, request, uuid=None):
        """Get stock information corresponding to this product"""
        product = get_object_or_404(self.product_queryset, uuid=uuid)
        stock = get_object_or_404(Stock, product_id=product.id)
        serializer = ProductListStockSerializer(stock)
        return Response(serializer.data, status=200)

    @extend_schema(
        description="Retrieves Sale Information for a particular Product.",
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Product.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            status.HTTP_200_OK: SalesResponseSerializer(many=True),
            status.HTTP_404_NOT_FOUND: ProductNotFoundSerializer,
        },
    )
    @action(detail=True, methods=["GET"])
    def sale_information(self, request, uuid=None):
        """Get sale information corresponding to this product"""
        product = get_object_or_404(self.product_queryset, uuid=uuid)
        product_sales = ProductSales.objects.filter(product=product).order_by("sale__created_at")
        sales = []
        for product_sale in product_sales:
            sale_data = {
                "uuid": product_sale.sale.uuid,
                "customer": product_sale.sale.customer.name,
                "employee": product_sale.sale.employee.user.first_name
                + " "
                + product_sale.sale.employee.user.last_name,
                "payment": dict(PaymentMode.PaymentMethod.choices)[product_sale.sale.payment.payment_method],
                "sale_status": dict(Sales.TransactionProgress.choices)[product_sale.sale.sale_status],
                "created_at": product_sale.sale.created_at,
                "quantity_sold": product_sale.quantity_sold,
                "price_per_unit": product_sale.price_per_unit,
                "price": product_sale.price,
            }
            if sale_data not in sales:
                sales.append(sale_data)
        return Response(
            sales,
            status=200,
        )

    @extend_schema(
        description="Retrieves Purchase Information for a particular Product.",
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this Product.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            status.HTTP_404_NOT_FOUND: ProductNotFoundSerializer,
        },
    )
    @action(detail=True, methods=["GET"])
    def purchase_information(self, request, uuid=None):
        """
        Get purchase information corresponding to this product
        """
        product = get_object_or_404(self.product_queryset, uuid=uuid)
        product_purchases = PurchaseProduct.objects.filter(product=product).order_by("purchase__created_at")
        purchases = []
        seen_product_purchase_uuids = set()
        for product_purchase in product_purchases:
            if product_purchase.uuid in seen_product_purchase_uuids:
                continue
            purchase_data = {
                "uuid": product_purchase.purchase.uuid,
                "supplier": product_purchase.supplier.name,
                "employee": product_purchase.purchase.employee.user.first_name
                + " "
                + product_purchase.purchase.employee.user.last_name,
                "quantity": product_purchase.product_quantity,
                "unit_price": product_purchase.purchase_unit_price,
                "total_cost": product_purchase.total_product_cost,
                "discount": product_purchase.discount_applied,
                "created_at": product_purchase.created_at,
            }
            purchases.append(purchase_data)
        return Response(purchases, status=200)


@response_schema(serializer=StockResponseSerializer)
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
        serializer = StockSerializer(data=request.data)
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
        request=GenerateStockMovementReportSerializer,
    )
    @action(detail=False, methods=["POST"])
    def generate_stock_movement_report(self, request):
        """
        Generate stock movement report for a given date range
        """
        data = request.data
        start_date = data.get("start_date", None)
        end_date = data.get("end_date", None)
        if start_date and end_date:
            start_date = make_aware(datetime.strptime(start_date, "%Y-%m-%d")).date()
            end_date = make_aware(datetime.strptime(end_date, "%Y-%m-%d")).date()
        else:
            return Response(
                {"message": "Please provide a start date and end date"},
                status=400,
            )

        # Filter stock items based on the date range
        stock_movements = StockMovement.objects.filter(created_at__date__range=[start_date, end_date])

        if not stock_movements:
            return Response(
                {"message": "No stock movement found for the given date range"},
                status=400,
            )

        report = {
            "start_date": start_date,
            "end_date": end_date,
            "stock_movement": [],
        }

        seen_stock_movement_uuids = set()

        for stock_movement in stock_movements:
            stock_uuid = stock_movement.stock.uuid
            stock_movement_uuid = stock_movement.uuid
            if stock_movement_uuid in seen_stock_movement_uuids:
                continue
            stock_movement_serializer = StockMovementSansStockResponseSerializer(stock_movement)
            response = {
                **stock_movement_serializer.data,
                "stock_uuid": stock_uuid,
                "product_name": stock_movement.stock.product.name,
                "stock_quantity": stock_movement.stock.stock_quantity,
                "stock_updated_at": stock_movement.stock.updated_at,
                "cost_per_unit": stock_movement.stock.cost_per_unit,
                "price_per_unit_retail": stock_movement.stock.price_per_unit_retail,
                "price_per_unit_wholesale": stock_movement.stock.price_per_unit_wholesale,
                "reorder_level": stock_movement.stock.reorder_level,
                "reorder_quantity": stock_movement.stock.reorder_quantity,
            }
            report["stock_movement"].append(response)
            seen_stock_movement_uuids.add(stock_movement_uuid)
        return Response(
            {"stock_movement_report": report},
            status=200,
        )

    @extend_schema(
        description="Retrieves a list of Products according to query.",
        request=StockSearchSerializer,
        responses={
            status.HTTP_200_OK: StockResponseSerializer(many=True),
        },
    )
    @action(detail=False, methods=["POST"])
    def search(self, request, *args, **kwargs):
        """
        Returns stock information using product name, description or code  in query
        """
        serializer = StockSearchSerializer(data=request.data)
        if serializer.is_valid():
            search_results = serializer.search_stock()
            return Response(search_results, status=200)
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
        request=StockMovementAvecProductSerializer,
        responses={status.HTTP_200_OK: StockMovementAvecProductResponseSerializer(many=True)},
    )
    @action(detail=True, methods=["GET"])
    def list_all_stock_movements(self, request, uuid=None):
        """
        Returns a list of all stock movements associated with a particular stock
        """
        stock = get_object_or_404(self.stock_queryset, uuid=uuid)
        stock_movements = stock.movement.all()
        movements = []
        seen_stock_movements_uuids = set()
        for stock_movement in stock_movements:
            stock_movement_uuid = stock_movement.uuid
            if stock_movement_uuid in seen_stock_movements_uuids:
                continue
            stock_movement_serializer = StockMovementSansStockResponseSerializer(stock_movement)
            response = {
                **stock_movement_serializer.data,
                "product": stock_movement.stock.product.name,
            }
            movements.append(response)
            seen_stock_movements_uuids.add(stock_movement_uuid)
        return Response(movements, status=200)


@response_schema(serializer=StockMovementResponseSerializer)
class StockMovementViewSet(ViewSet):
    """
    API endpoint allowing stock_movement data be viewed, created and
    or edited
    """

    serializer_class = StockMovementSerializer
    lookup_field = "uuid"

    @property
    def stock_movement_queryset(self):
        return StockMovement.objects.all()

    @property
    def stock_queryset(self):
        return Stock.objects.all()

    def list(self, request, uuid=None):
        """
        List all StockMovements
        """
        serializer = StockMovementSerializer(self.stock_movement_queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this StockMovement",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, uuid=None):
        """
        Retun a single StockMovement
        """
        stock_movement = get_object_or_404(self.stock_movement_queryset, uuid=uuid)
        serializer = StockMovementSerializer(stock_movement)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new StockMovement"""
        serializer = StockMovementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this StockMovement.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, uuid=None):
        """Update a StockMovement"""
        stock_movement = get_object_or_404(self.stock_movement_queryset, uuid=uuid)
        serializer = StockMovementSerializer(stock_movement, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this StockMovement.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, uuid=None):
        """Update a StockMovement"""
        stock_movement = get_object_or_404(self.stock_movement_queryset, uuid=uuid)
        serializer = StockMovementSerializer(stock_movement, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this StockMovement.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, uuid=None):
        """Delete a StockMovement"""
        stock_movement = get_object_or_404(self.stock_movement_queryset, uuid=uuid)
        stock_movement.delete()
        return Response(status=204)


@response_schema(serializer=SupplierProductResponseSerializer)
class SupplierProductViewSet(ViewSet):
    """
    API endpoint that allows suppliers to be viewed or edited.
    """

    serializer_class = SupplierProductSerializer
    lookup_field = "uuid"

    @property
    def supplier_queryset(self):
        return Supplier.objects.all()

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
        serializer = SupplierProductSerializer(self.supplier_product_queryset, many=True)
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
        supplier_product = get_object_or_404(self.supplier_product_queryset, uuid=uuid)
        serializer = SupplierProductSerializer(supplier_product)
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
        supplier_product = get_object_or_404(self.supplier_product_queryset, uuid=uuid)
        serializer = SupplierProductSerializer(supplier_product, data=request.data)
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
        supplier_product = get_object_or_404(self.supplier_product_queryset, uuid=uuid)
        serializer = SupplierProductSerializer(supplier_product, data=request.data, partial=True)
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
        supplier_product = get_object_or_404(self.supplier_product_queryset, uuid=uuid)
        supplier_product.delete()
        return Response(status=204)


@response_schema(serializer=SupplierResponseSerializer)
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
        serializer = SupplierSerializer(data=request.data)
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
        responses={
            status.HTTP_200_OK: SupplierListAllProductsSerializer,
            status.HTTP_404_NOT_FOUND: ProductNotFoundSerializer,
        },
    )
    @action(detail=True, methods=["GET"])
    def list_all_products(self, request, uuid=None):
        """
        List all Products associated with a Supplier
        """
        supplier = get_object_or_404(self.supplier_queryset, uuid=uuid)
        supplier_products = supplier.supplierproduct_set.all()
        products = []
        for supplier_product in supplier_products:
            product = {
                "category": supplier_product.product.category.name,
                "name": supplier_product.product.name,
                "uuid": supplier_product.product.uuid,
                "code": supplier_product.product.code,
                "description": supplier_product.product.description,
                "product_type": str(dict(Product.ProductType.choices)[supplier_product.product.product_type]),
                "tax_type": str(dict(Product.TaxType.choices)[supplier_product.product.tax_type]),
                "packaging_unit": str(dict(Product.PackagingUnit.choices)[supplier_product.product.packaging_unit]),
                "unit": str(dict(Product.UnitOfQuantity.choices)[supplier_product.product.unit]),
                "limited": supplier_product.product.limited,
                "active_for_sale": supplier_product.product.active_for_sale,
            }
            if product not in products:
                products.append(product)
        serializer = SupplierListAllProductsSerializer(data=products, many=True)
        if serializer.is_valid():
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)
