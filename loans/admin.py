# loans/admin.py
from django.contrib import admin
from django.db import models
from .models import LoanApplication, LoanRepayment

@admin.register(LoanApplication)
class LoanApplicationAdmin(admin.ModelAdmin):
    list_display = ('farmer', 'amount_requested', 'amount_approved', 'status', 
                   'date_applied', 'repayment_period_months', 'get_interest', 'balance')
    list_filter = ('status',)
    list_editable = ('amount_approved', 'status')
    search_fields = ('farmer__username', 'farmer__email')
    ordering = ('-date_applied',)
    actions = ['approve_loans', 'reject_loans', 'disburse_loans']
    
    def get_interest(self, obj):
        if not obj.amount_approved:
            return 0
        total_repaid = obj.repayments.aggregate(models.Sum('amount_paid'))['amount_paid__sum'] or 0
        outstanding = obj.amount_approved - total_repaid
        return round(outstanding * obj.interest_rate, 2)
    get_interest.short_description = 'Interest'
    
    @admin.action(description='Approve selected loans')
    def approve_loans(self, request, queryset):
        updated = queryset.update(status='APPROVED')
        self.message_user(request, f"{updated} loan(s) successfully approved.")
    
    @admin.action(description='Reject selected loans')
    def reject_loans(self, request, queryset):
        updated = queryset.update(status='REJECTED')
        self.message_user(request, f"{updated} loan(s) successfully rejected.")
    
    @admin.action(description='Mark selected loans as Disbursed')
    def disburse_loans(self, request, queryset):
        updated = queryset.filter(status='APPROVED').update(status='DISBURSED')
        self.message_user(request, f"{updated} loan(s) successfully marked as disbursed.")

@admin.register(LoanRepayment)
class LoanRepaymentAdmin(admin.ModelAdmin):
    list_display = ('loan', 'get_amount_approved', 'amount_paid', 'payment_date')
    search_fields = ('loan__farmer__username',)
    ordering = ('-payment_date',)
    
    def get_amount_approved(self, obj):
        return obj.loan.amount_approved
    get_amount_approved.short_description = 'Amount Approved'