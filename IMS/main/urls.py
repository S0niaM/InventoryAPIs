

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import InventoryItemViewSet, Register, Login

router = DefaultRouter()
router.register(r'items', InventoryItemViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
]