"""
Module illustrating the viewsets for administration API's
"""
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from administration.models import Business, Employee, Owner
from .serializers import (
    BusinessSerializer,
    EmployeeSerializer,
    OwnerSerializer,
    OwnerResponseSerializer,
    AdministrationNotFoundSerializer,
)
from pos_inventory.utils.decorators import response_schema


@response_schema(serializer=OwnerResponseSerializer)
class OwnerViewset(ViewSet):
    """
    API endpoint that allows Business Owner to be created, viewed and or edited
    NB: Kindly note that this view should be limited to Admin and Maube owner alone
    """

    serializer_class = OwnerSerializer
    lookup_field = "uuid"

    @property
    def queryset(self):
        return Owner.objects.all()

    def list(self, request, *args, **kwargs):
        """
        Returns a lists of business owners
        """
        serializer = OwnerSerializer(self.queryset, many=True)
        return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this owner.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            status.HTTP_404_NOT_FOUND: AdministrationNotFoundSerializer,
        },
    )
    def retrieve(self, request, uuid=None):
        """Retrieves a owner given its associated identifier"""
        owner = get_object_or_404(self.queryset, uuid=uuid)
        serializer = OwnerSerializer(owner)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a  new owner"""
        print(f"data to create owner is {request.data}")
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this owner.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            status.HTTP_404_NOT_FOUND: AdministrationNotFoundSerializer,
        },
    )
    def update(self, request, uuid=None):
        """Updates a owner given its associated identifier"""
        owner = get_object_or_404(self.queryset, uuid=uuid)
        serializer = OwnerSerializer(owner, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this owner.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            status.HTTP_404_NOT_FOUND: AdministrationNotFoundSerializer,
        },
    )
    def partial_update(self, request, uuid=None):
        """updates a owner partially given it's identifier"""
        owner = get_object_or_404(self.queryset, uuid=uuid)
        serializer = OwnerSerializer(owner, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="uuid",
                description="A unique identifier identifying this owner.",
                required=True,
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.PATH,
            )
        ],
        responses={
            status.HTTP_404_NOT_FOUND: AdministrationNotFoundSerializer,
        },
    )
    def destroy(self, request, uuid=None):
        """deletes an existing owner"""
        owner = get_object_or_404(self.queryset, uuid=uuid)
        owner.user.delete()
        owner.delete()
        # find out how to return an empty object
        return Response({}, status=204)

    # TODO: Write a function that allows one to create multiple users at once and link them
    # to a business


class BusinessViewset(ViewSet):
    """
    API endpoint that allows Business to be viewed or edited
    NB: Kindly note that this view should be limited to Admin and Maube owner alone
    """

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
        responses={
            status.HTTP_404_NOT_FOUND: AdministrationNotFoundSerializer,
        },
    )
    def retrieve(self, request, uuid=None):
        """Retrieves a business given its associated identifier"""
        business = get_object_or_404(self.queryset, uuid=uuid)
        serializer = BusinessSerializer(business)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """Creates a  new business"""
        data = request.data
        serializer = BusinessSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
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
        responses={
            status.HTTP_404_NOT_FOUND: AdministrationNotFoundSerializer,
        },
    )
    def update(self, request, uuid=None):
        """Updates a business given its associated identifier"""
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
        responses={
            status.HTTP_404_NOT_FOUND: AdministrationNotFoundSerializer,
        },
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
        responses={
            status.HTTP_404_NOT_FOUND: AdministrationNotFoundSerializer,
        },
    )
    def destroy(self, request, uuid=None):
        """deletes an existing business"""
        business = get_object_or_404(self.queryset, uuid=uuid)
        business.delete()
        return Response({}, status=204)

    @action(detail=True, methods=["GET"])
    def list_all_owners(self, request, uuid=None):
        """
        Lists all owners of the business
        """
        business = get_object_or_404(self.queryset, uuid=uuid)
        owners = business.owners.all()
        serializer = OwnerSerializer(owners, many=True)
        return Response(serializer.data)


class EmployeeViewset(ViewSet):
    """
    API endpoint that allows employee to be viewed or edited
    """

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
        if employee:
            employee.user.delete()
            employee.delete()
            return Response({}, status=204)
        return
