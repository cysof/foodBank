# loans/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LoanApplicationViewSet, LoanRepaymentViewSet

router = DefaultRouter()
router.register(r'loan-applications', LoanApplicationViewSet, basename='loan-application')
router.register(r'loan-repayments', LoanRepaymentViewSet, basename='loan-repayment')

urlpatterns = [
    path('', include(router.urls)),
]
