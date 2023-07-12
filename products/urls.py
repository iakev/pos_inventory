from products.api.v1.viewsets import ProductViewSet
from products.api.v1.viewsets import CategoryViewSet
from products.api.v1.viewsets import StockViewSet
from products.api.v1.viewsets import SupplierViewSet
from products.api.v1.viewsets import SupplierProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"products", ProductViewSet, basename="product")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"stocks", StockViewSet, basename="stock")
router.register(r"suppliers", SupplierViewSet, basename="supplier")
router.register(r"supplier_products", SupplierProductViewSet, basename="supplier_products")
urlpatterns = router.urls
