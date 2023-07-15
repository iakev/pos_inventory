from sales.api.v1.viewsets import SalesViewSet, CustomerViewset
from sales.api.v1.viewsets import ProductSalesViewset, PaymentModeViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"sales", SalesViewSet, basename="sales")
router.register(r"productsales", ProductSalesViewset, basename="productsales")
router.register(r"customers", CustomerViewset, basename="customers")
router.register(r"paymentmodes", PaymentModeViewSet, basename="paymentmodes")

urlpatterns = router.urls
