"""
Module illustrating the viewsets for administration API's
"""
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from administration.models import Business, Customer, Employee
from .serializers import BusinessSerializer, CustomerSerializer, EmployeeSerializer


class BusinessViewset(ViewSet):
    """API endpoint that allows Business to be viewed or edited"""

    queryset = Business.objects.all()

    def list(self, request, *args, **kwargs):
        """Returns a list of business"""
        serializer = BusinessSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieves a business given its associated identifier"""
        business = get_object_or_404(self.queryset, uuid=pk)
        serializer = BusinessSerializer(business)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a  new business"""
        serializer = BusinessSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        """Updates a business given its associated identifier"""
        business = get_object_or_404(self.queryset, uuid=pk)
        serializer = BusinessSerializer(business, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """updates a business partially given it's identifier"""
        business = get_object_or_404(self.queryset, uuid=pk)
        serializer = BusinessSerializer(business, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """deletes an existing business"""
        business = get_object_or_404(self.queryset, uuid=pk)
        business.delete()
        return Response(status=204)


class CustomerViewset(ViewSet):
    """API endpoint that allows customer to be viewed or edited"""

    queryset = Customer.objects.all()

    def list(self, request, *args, **kwargs):
        """Returns a list of Customer"""
        serializer = CustomerSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieves a Customer given its associated identifier"""
        customer = get_object_or_404(self.queryset, uuid=pk)
        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a  new customer"""
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        """Updates a Customer given its associated identifier"""
        customer = get_object_or_404(self.queryset, uuid=pk)
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """updates a customer partially given it's identifier"""
        customer = get_object_or_404(self.queryset, uuid=pk)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """deletes an existing Customer"""
        customer = get_object_or_404(self.queryset, uuid=pk)
        customer.delete()
        return Response(status=204)


class EmployeeViewset(ViewSet):
    """API endpoint that allows employee to be viewed or edited"""

    queryset = Employee.objects.all()

    def list(self, request, *args, **kwargs):
        """Returns a list of employee"""
        serializer = EmployeeSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Retrieves a employee given its associated identifier"""
        employee = get_object_or_404(self.queryset, uuid=pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a  new employee"""
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    def update(self, request, pk=None):
        """Updates a Employee given its associated identifier"""
        employee = get_object_or_404(self.queryset, uuid=pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def partial_update(self, request, pk=None):
        """updates a employee partially given it's identifier"""
        employee = get_object_or_404(self.queryset, uuid=pk)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def destroy(self, request, pk=None):
        """deletes an existing Employee"""
        employee = get_object_or_404(self.queryset, uuid=pk)
        employee.delete()
        return Response(status=204)
