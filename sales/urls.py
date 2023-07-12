from sales.api.v1.viewsets import SalesViewSet, CustomerViewset
from sales.api.v1.viewsets import ProductSalesViewset

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"sales", SalesViewSet, basename="sales")
router.register(r"productsales", ProductSalesViewset, basename="productsales")
router.register(r"customers", CustomerViewset, basename="customers")

urlpatterns = router.urls
