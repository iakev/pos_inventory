from sales.api.v1.viewsets import (
    SalesViewSet,
    ProductSalesViewset,
    CustomerViewset,
    PaymentModeViewSet,
    PurchaseViewset
)
from products.api.v1.viewsets import ProductViewSet, CategoryViewSet, StockViewSet
from products.api.v1.viewsets import (
    ProductViewSet,
    CategoryViewSet,
    StockViewSet,
    SupplierViewSet,
    SupplierProductViewSet,
)
from administration.api.v1.viewsets import BusinessViewset, EmployeeViewset
from pos_inventory.users.api.viewsets import UserViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"sales", SalesViewSet, basename="sales")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"stocks", StockViewSet, basename="stock")
router.register(r"productsales", ProductSalesViewset, basename="productsales")
router.register(r"business", BusinessViewset, basename="business")
router.register(r"customers", CustomerViewset, basename="customers")
router.register(r"employees", EmployeeViewset, basename="employees")
router.register(r"suppliers", SupplierViewSet, basename="supplier")
router.register(
    r"supplierproducts", SupplierProductViewSet, basename="supplierproducts"
)
router.register(r"paymentmodes", PaymentModeViewSet, basename="paymentmodes")
router.register(r"purchases", PurchaseViewset, basename="purchases")
router.register(r"users", UserViewSet, basename="users")

urlpatterns = router.urls
