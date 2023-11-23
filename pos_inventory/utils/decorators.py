from rest_framework import serializers
from rest_framework import status
from drf_spectacular.utils import extend_schema, extend_schema_view


class NotFoundSerializer(serializers.Serializer):
    detail = serializers.CharField(default="Unfortunately requested resource not found")


def response_schema(**kwargs):
    def decorator(view):
        extend_schema_view(
            list=extend_schema(
                responses={
                    status.HTTP_200_OK: kwargs["serializer"],
                    status.HTTP_404_NOT_FOUND: NotFoundSerializer,
                }
            ),
            retrieve=extend_schema(
                responses={
                    status.HTTP_200_OK: kwargs["serializer"],
                    status.HTTP_404_NOT_FOUND: NotFoundSerializer,
                }
            ),
            create=extend_schema(
                responses={
                    status.HTTP_201_CREATED: kwargs["serializer"],
                    status.HTTP_404_NOT_FOUND: NotFoundSerializer,
                }
            ),
            update=extend_schema(
                responses={
                    status.HTTP_200_OK: kwargs["serializer"],
                    status.HTTP_404_NOT_FOUND: NotFoundSerializer,
                }
            ),
            partial_update=extend_schema(
                responses={
                    status.HTTP_200_OK: kwargs["serializer"],
                    status.HTTP_404_NOT_FOUND: NotFoundSerializer,
                }
            ),
        )(view)
        return view

    return decorator
