from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import SpendingViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'spendings', SpendingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
