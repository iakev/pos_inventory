from sales.api.v1.viewsets import SalesViewSet, ProductSalesViewset
from products.api.v1.viewsets import ProductViewSet, CategoryViewSet, StockViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"sales", SalesViewSet, basename="sales")
router.register(r"products", ProductViewSet, basename="products")
router.register(r"categories", CategoryViewSet, basename="categories")
router.register(r"stocks", StockViewSet, basename="stock")
router.register(r"productsales", ProductSalesViewset, basename="productsales")

urlpatterns = router.urls
