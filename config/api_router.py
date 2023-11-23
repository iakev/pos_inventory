from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from pos_inventory.users.api.views import UserViewSet
from sales.api.v1.viewsets import (
    SalesViewSet,
    ProductSalesViewset,
    CustomerViewset,
    PaymentModeViewSet,
    PurchaseViewSet,
    PurchaseProductViewSet,
)
from products.api.v1.viewsets import (
    ProductViewSet,
    CategoryViewSet,
    StockViewSet,
    SupplierViewSet,
    SupplierProductViewSet,
    StockMovementViewSet,
)
from administration.api.v1.viewsets import (
    BusinessViewset,
    EmployeeViewset,
    OwnerViewset,
)
from pos_inventory.users.api.viewsets import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"owners", OwnerViewset, basename="owners")
router.register(r"sales", SalesViewSet, basename="sales")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"stocks", StockViewSet, basename="stock")
router.register(r"stockmovement", StockMovementViewSet, basename="stockmovement")
router.register(r"productsales", ProductSalesViewset, basename="productsales")
router.register(r"business", BusinessViewset, basename="business")
router.register(r"customers", CustomerViewset, basename="customers")
router.register(r"employees", EmployeeViewset, basename="employees")
router.register(r"suppliers", SupplierViewSet, basename="supplier")
router.register(r"supplierproducts", SupplierProductViewSet, basename="supplierproducts")
router.register(r"paymentmodes", PaymentModeViewSet, basename="paymentmodes")
router.register(r"purchases", PurchaseViewSet, basename="purchases")
router.register(r"purchaseproducts", PurchaseProductViewSet, basename="purchaseproducts")
router.register(r"users", UserViewSet, basename="users")

urlpatterns = router.urls

app_name = "api"
