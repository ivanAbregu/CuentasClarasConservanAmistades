from rest_framework.routers import SimpleRouter

from .views import OrderViewSet, PaymentViewSet

router = SimpleRouter()

router.register("order", OrderViewSet)
router.register("payment", PaymentViewSet)

urlpatterns = router.urls
