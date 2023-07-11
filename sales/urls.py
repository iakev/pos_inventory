from sales.api.v1.viewsets import SalesViewSet
from sales.api.v1.viewsets import ProductSalesViewset

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"sales", SalesViewSet, basename="sales")
router.register(r"productsales", ProductSalesViewset, basename="productsales")

urlpatterns = router.urls
