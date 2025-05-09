from rest_framework import serializers
from django.db import models
from .models import LoanApplication, LoanRepayment

class LoanRepaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRepayment
        fields = [
            'id', 'loan', 'amount_paid', 'payment_date', 'payment_method'
        ]
        read_only_fields = ['payment_date']
        # Remove 'interest_amount' since it doesn't exist in your model

class LoanApplicationSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()
    interest = serializers.SerializerMethodField()
    
    class Meta:
        model = LoanApplication
        fields = [
            'id', 'farmer', 'farm', 'amount_requested', 'amount_approved',
            'purpose', 'repayment_period_months', 'status',
            'date_applied', 'date_updated', 'balance', 'interest_rate', 'interest', 'repayments'
        ]
        read_only_fields = ['status', 'amount_approved', 'date_applied', 'date_updated', 'balance', 'interest']
    
    def get_interest(self, obj):
        if not obj.amount_approved:
            return 0
        total_repaid = obj.repayments.aggregate(models.Sum('amount_paid'))['amount_paid__sum'] or 0
        return (obj.amount_approved - total_repaid) * obj.interest_rate