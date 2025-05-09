from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'investments', views.InvestmentViewSet, basename='investment')

urlpatterns = [
    path('', include(router.urls)),
]