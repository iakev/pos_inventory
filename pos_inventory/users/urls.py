from django.urls import path

from pos_inventory.users.api.viewsets import UserViewSet
from rest_framework.routers import DefaultRouter


from pos_inventory.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
)

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
