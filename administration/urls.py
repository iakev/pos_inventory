from administration.api.v1.viewsets import (
    BusinessViewset,
    EmployeeViewset,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"business", BusinessViewset, basename="business")
router.register(r"employee", EmployeeViewset, basename="employee")
urlpatterns = router.urls
