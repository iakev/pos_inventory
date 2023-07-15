"""
Module illustrating the viewsets for product API's
"""
from administration.models import Supplier
from django.shortcuts import get_object_or_404, get_list_or_404
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

    @property
    def queryset(self):
        return Category.objects.all()

    def list(self, request, *args, **kwargs):
        """Return a list of all categories"""
        serializer = CategorySerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Return a single category"""
        category = get_object_or_404(self.queryset, uuid=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new category"""
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        """Update an existing category"""
        category = get_object_or_404(self.queryset, uuid=pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """Update an existing category"""
        category = get_object_or_404(self.queryset, uuid=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """Delete an existing category"""
        category = get_object_or_404(self.queryset, uuid=pk)
        category.delete()
        return Response(status=204)


class ProductViewSet(ViewSet):
    """Basic viewset for Product Related Items"""

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

    def retrieve(self, request, pk=None):
        """Return a single product"""
        product = get_object_or_404(self.product_queryset, uuid=pk)
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

    def update(self, request, pk=None):
        """Update an existing product"""
        product = get_object_or_404(self.product_queryset, uuid=pk)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """Update an existing product"""
        product = get_object_or_404(self.product_queryset, uuid=pk)
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """Delete an existing product"""
        product = get_object_or_404(self.product_queryset, uuid=pk)
        product.delete()
        return Response(status=204)


class StockViewSet(ViewSet):
    """ViewSet for Stock  Items"""

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

    def retrieve(self, request, pk=None):
        """Return a single stock"""
        stock = get_object_or_404(self.stock_queryset, uuid=pk)
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

    def update(self, request, pk=None):
        """Update an existing stock"""
        stock = get_object_or_404(self.stock_queryset, uuid=pk)
        serializer = StockSerializer(stock, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """Update an existing stock"""
        stock = get_object_or_404(self.stock_queryset, uuid=pk)
        serializer = StockSerializer(stock, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """Delete an existing stock"""
        stock = get_object_or_404(self.stock_queryset, uuid=pk)
        stock.delete()
        return Response(status=204)

    def switch_case(case, product_id, data):
        """
        Updating stock quantity according to the stock_movement quantity
        """
        stock = get_object_or_404(Stock.objects.all(), product_id=product_id)

    @action(detail=True, methods=["POST"])
    def stock_movement(self, request, pk=None):
        stock = get_object_or_404(self.stock_queryset, uuid=pk)

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


class SupplierProductViewSet(ViewSet):
    """
    API endpoint that allows suppliers to be viewed or edited.
    """

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

    def retrieve(self, request, pk=None):
        """
        Retun a single ProductSale
        """
        product_sale = get_object_or_404(self.supplier_product_queryset, uuid=pk)
        serializer = SupplierProductSerializer(product_sale)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new ProductSale"""
        serializer = SupplierProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        """Update a ProductSale"""
        product_sale = get_object_or_404(self.supplier_product_queryset, uuid=pk)
        serializer = SupplierProductSerializer(product_sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """Update a ProductSale"""
        product_sale = get_object_or_404(self.supplier_product_queryset, uuid=pk)
        serializer = SupplierProductSerializer(
            product_sale, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """Delete a ProductSale"""
        product_sale = get_object_or_404(self.supplier_product_queryset, uuid=pk)
        product_sale.delete()
        return Response(status=204)

    @action(detail=False, methods=["GET"])
    def list_all_supplier_products(self, request, pk=None):
        """
        List all ProductSales for a Sale
        """
        supplier = get_object_or_404(self.supplier_queryset, uuid=pk)
        supplier_products = get_list_or_404(
            self.supplier_product_queryset, supplier=supplier.id
        )
        serializer = SupplierProductSerializer(supplier_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def list_all_product_supplier(self, request, pk=None):
        """
        List all sales associated with a Product
        """
        product = get_object_or_404(self.product_queryset, uuid=pk)
        product_supplier = get_list_or_404(
            self.supplier_product_queryset, product=product.id
        )
        serializer = SupplierProductSerializer(product_supplier, many=True)
        return Response(serializer.data)


class SupplierViewSet(ViewSet):
    """API endpoit that allows Suppliers to be viewed and edited"""

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

    def retrieve(self, request, pk=None):
        """Return a single supplier"""
        supplier = get_object_or_404(self.supplier_queryset, uuid=pk)
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

    def update(self, request, pk=None):
        """Update an existing supplier"""
        supplier = get_object_or_404(self.supplier_queryset, uuid=pk)
        serializer = SupplierSerializer(supplier, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """Update an existing supplier partially"""
        supplier = get_object_or_404(self.supplier_queryset, uuid=pk)
        serializer = SupplierSerializer(supplier, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """Delete an existing supplier"""
        supplier = get_object_or_404(self.supplier_queryset, uuid=pk)
        supplier.delete()
        return Response(status=204)
