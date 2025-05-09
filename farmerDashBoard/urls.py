from django.urls import path, include
from rest_framework import routers
from .views import (
    FarmerDashboardView,
    FarmViewSet,
    CropViewSet,
    FarmingSeasonViewSet,
    FinancialsView,
    PayoutRequestView,
    PayoutViewSet,
    MarketTrendViewSet,
)

router = routers.DefaultRouter()

router.register(r'farms', FarmViewSet, basename='farm')
router.register(r'crops', CropViewSet, basename='crop')
router.register(r'farming-seasons', FarmingSeasonViewSet, basename='farming-season')
router.register(r'payouts', PayoutViewSet, basename='payout')
router.register(r'market-trends', MarketTrendViewSet, basename='market-trend')

urlpatterns = [
    path('farmer-dashboard/', FarmerDashboardView.as_view(), name='farmer-dashboard'),
    path('financials/', FinancialsView.as_view(), name='financials'),
    path('payout-request/', PayoutRequestView.as_view(), name='payout-request'),
    path('', include(router.urls)),
]