from rest_framework.routers import SimpleRouter

from .views import BeerViewSet

router = SimpleRouter()

router.register("Beer", BeerViewSet)

urlpatterns = router.urls
