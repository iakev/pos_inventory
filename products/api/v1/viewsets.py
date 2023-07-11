"""
Module illustrating the viewsets for product API's
"""
from decimal import Decimal
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.viewsets import ViewSet

from products.models import Product, Category, Stock
from .serializers import ProductSerializer, CategorySerializer, StockSerializer


class CategoryViewSet(ViewSet):
    """Basic viewset for Category Related Items"""
    queryset = Category.objects.all()

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
    product_queryset = Product.objects.all()
    category_queryset = Category.objects.all()

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
        print(f"data is {data}")
        uuid = data.get('category', None)
        print(f"uuid is {uuid}")
        if uuid:
            print(uuid)
            category = get_object_or_404(self.category_queryset, uuid=uuid)
            print(f"the category is {category}")
            data['category'] = category.id
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

    stock_queryset = Stock.objects.all()
    product_queryset = Product.objects.all()

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
    
    @action(detail=True, methods=['POST'])
    def stock_movement(self, request, pk=None):
        stock = get_object_or_404(self.stock_queryset, uuid=pk)

        stock_movement_type = request.data.get('stock_movement_type')
        stock_movement_quantity = request.data.get('stock_movement_quantity')
        stock_movement_remarks = request.data.get('stock_movement_remarks')
        print(request.data)
        if stock_movement_type:
            stock.update_stock_quantity(stock_movement_type, stock_movement_quantity, stock_movement_remarks)
            serializer = StockSerializer(stock, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)
        return Response({'error': 'No stock movement type given'}, status=400)
