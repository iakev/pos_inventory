"""
Model defining viewsets for Sales API's
"""
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from products.models import Product
from sales.models import PaymentMode, ProductSales, Sales
from .serializers import PaymentModeSerializer, ProductSalesSerializer, SalesSerializer


class SalesViewSet(ViewSet):
    """
    API endpoint that allows Sales to be viewed or edited.
    """

    queryset = Sales.objects.all()

    def list(self, request, *args, **kwargs):
        """
        List all Sales.
        """
        serializer = SalesSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieve a Sale indentified by uuid"""
        sale = get_object_or_404(self.queryset, uuid=pk)
        serializer = SalesSerializer(sale)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new Sale"""
        serializer = SalesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        """Update a Sale"""
        sale = get_object_or_404(self.queryset, uuid=pk)
        serializer = SalesSerializer(sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """Update a Sale"""
        sale = get_object_or_404(self.queryset, uuid=pk)
        serializer = SalesSerializer(sale, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """Delete a Sale"""
        sale = get_object_or_404(self.queryset, uuid=pk)
        sale.delete()
        return Response(status=204)


class ProductSalesViewset(ViewSet):
    """
    API endpoint that allows Product to be viewed or edited.
    """

    product_queryset = Product.objects.all()
    sales_queryset = Sales.objects.all()
    product_sales_queryset = ProductSales.objects.all()

    def list(self, request, *args, **kwargs):
        """
        List all ProductSales.
        """
        serializer = ProductSalesSerializer(self.sales_queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Retun a single ProductSale
        """
        product_sale = get_object_or_404(self.product_sales_queryset, uuid=pk)
        serializer = ProductSalesSerializer(product_sale)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Create a new ProductSale"""
        serializer = ProductSalesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        """Update a ProductSale"""
        product_sale = get_object_or_404(self.product_sales_queryset, uuid=pk)
        serializer = ProductSalesSerializer(product_sale, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """Update a ProductSale"""
        product_sale = get_object_or_404(self.product_sales_queryset, uuid=pk)
        serializer = ProductSalesSerializer(
            product_sale, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """Delete a ProductSale"""
        product_sale = get_object_or_404(self.product_sales_queryset, uuid=pk)
        product_sale.delete()
        return Response(status=204)

    @action(detail=False, methods=["GET"])
    def list_all_sale_products(self, request, pk=None):
        """
        List all ProductSales for a Sale
        """
        sale = get_object_or_404(self.sales_queryset, uuid=pk)
        product_sales = get_list_or_404(self.product_sales_queryset, sales=sale.id)
        serializer = ProductSalesSerializer(product_sales, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def list_all_product_sales(self, request, pk=None):
        """
        List all sales associated with a Product
        """
        product = get_object_or_404(self.product_queryset, uuid=pk)
        product_sales = get_list_or_404(self.product_sales_queryset, product=product.id)
        serializer = ProductSalesSerializer(product_sales, many=True)
        return Response(serializer.data)
