from products.api.v1.viewsets import ProductViewSet
from products.api.v1.viewsets import CategoryViewSet
from products.api.v1.viewsets import StockViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'stocks', StockViewSet, basename='stock')
urlpatterns = router.urls
