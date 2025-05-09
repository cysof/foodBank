# loans/views.py
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.db import models
from .models import LoanApplication, LoanRepayment
from .serializers import LoanApplicationSerializer, LoanRepaymentSerializer

class LoanApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = LoanApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return LoanApplication.objects.filter(farmer=self.request.user)
        return LoanApplication.objects.none()

    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        """Admin can approve or reject a loan."""
        loan = self.get_object()
        new_status = request.data.get('status')
        
        if new_status not in ['APPROVED', 'REJECTED']:
            return Response({"error": "Status must be 'APPROVED' or 'REJECTED'."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        loan.status = new_status
        loan.save()
        return Response({"message": f"Loan status updated to {loan.status}."})

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAdminUser])
    def update_status(self, request, pk=None):
        """Admin can update loan status to DISBURSED, REPAID, etc."""
        loan = self.get_object()
        new_status = request.data.get('status')

        allowed_statuses = ['DISBURSED', 'REPAID', 'DEFAULTED']
        if new_status not in allowed_statuses:
            return Response({"error": f"Status must be one of {allowed_statuses}."},
                            status=status.HTTP_400_BAD_REQUEST)

        loan.status = new_status
        loan.save()
        return Response({"message": f"Loan status changed to {loan.status}."})
    
    
    
class LoanRepaymentViewSet(viewsets.ModelViewSet):
    serializer_class = LoanRepaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return LoanRepayment.objects.filter(loan__farmer=self.request.user)
        return LoanRepayment.objects.none()

    def perform_create(self, serializer):
        loan = serializer.validated_data['loan']
        if loan.farmer != self.request.user:
            raise ValidationError("You can only repay your own loans.")
        serializer.save()

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def repay(self, request, pk=None):
        """Farmer repays a loan."""
        repayment = self.get_object()
        amount_repaid = request.data.get('amount_repaid')

        if amount_repaid is None:
            return Response({"error": "Amount repaid is required."},
                            status=status.HTTP_400_BAD_REQUEST)

        if amount_repaid <= 0:
            return Response({"error": "Amount repaid must be greater than zero."},
                            status=status.HTTP_400_BAD_REQUEST)

        loan = repayment.loan
        total_repaid = loan.repayments.aggregate(models.Sum('amount_paid'))['amount_paid__sum'] or 0
        outstanding_balance = loan.amount_requested - total_repaid

        if amount_repaid > outstanding_balance:
            return Response({"error": f"Amount repaid cannot be greater than the outstanding balance of {outstanding_balance}."},
                            status=status.HTTP_400_BAD_REQUEST)

        repayment.amount_paid = amount_repaid
        repayment.save()
        return Response({"message": f"Repayment of {amount_repaid} successful."})