"""
Module illustrating the viewsets for administration API's
"""
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from administration.models import Business, Employee
from .serializers import BusinessSerializer, EmployeeSerializer


class BusinessViewset(ViewSet):
    """API endpoint that allows Business to be viewed or edited"""

    serializer_class = BusinessSerializer
    lookup_field = "uuid"

    @property
    def queryset(self):
        return Business.objects.all()

    def list(self, request, *args, **kwargs):
        """Returns a list of business"""
        serializer = BusinessSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this business.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, uuid=None):
        """Retrieves a business given its associated identifier"""
        business = get_object_or_404(self.queryset, uuid=uuid)
        serializer = BusinessSerializer(business)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a  new business"""
        print("creating a new business")
        data = request.data
        print(data)
        serializer = BusinessSerializer(data=data)
        print("befor the serailizer validates")
        if serializer.is_valid():
            print("serializer valid before saving")
            serializer.save()
            print("after save method of serializer called")
            return Response(serializer.data, status=201)
        print("serializer invalid")
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this business.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, uuid=None):
        """Updates a business given its associated identifier"""
        print("updating a business")
        business = get_object_or_404(self.queryset, uuid=uuid)
        serializer = BusinessSerializer(business, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this business.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, uuid=None):
        """updates a business partially given it's identifier"""
        business = get_object_or_404(self.queryset, uuid=uuid)
        serializer = BusinessSerializer(business, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this business.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, uuid=None):
        """deletes an existing business"""
        business = get_object_or_404(self.queryset, uuid=uuid)
        business.delete()
        return Response({}, status=204)


class EmployeeViewset(ViewSet):
    """API endpoint that allows employee to be viewed or edited"""

    serializer_class = EmployeeSerializer
    lookup_field = "uuid"

    @property
    def queryset(self):
        return Employee.objects.all()

    def list(self, request, *args, **kwargs):
        """Returns a list of employee"""
        serializer = EmployeeSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this employee.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def retrieve(self, request, uuid=None):
        """Retrieves a employee given its associated identifier"""
        employee = get_object_or_404(self.queryset, uuid=uuid)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a  new employee"""
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this employee.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def update(self, request, uuid=None):
        """Updates a Employee given its associated identifier"""
        employee = get_object_or_404(self.queryset, uuid=uuid)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this employee.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def partial_update(self, request, uuid=None):
        """updates a employee partially given it's identifier"""
        employee = get_object_or_404(self.queryset, uuid=uuid)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            employee = serializer.update(employee, serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this employee.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
    )
    def destroy(self, request, uuid=None):
        """deletes an existing Employee"""
        employee = get_object_or_404(self.queryset, uuid=uuid)
        employee.delete()
        return Response(status=204)
