# loans/models.py
from django.db import models
from django.conf import settings
from farmerDashBoard.models import Farm, FarmingSeason

class LoanApplication(models.Model):
    LOAN_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DISBURSED', 'Disbursed'),
        ('REJECTED', 'Rejected'),
        ('REPAID', 'Repaid'),
    )
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loan_applications')
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='loan_applications')
    seassion = models.ForeignKey(FarmingSeason, on_delete=models.CASCADE, related_name='loan_applications')
    amount_requested = models.DecimalField(max_digits=12, decimal_places=2)
    amount_approved = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    purpose = models.TextField()
    repayment_period_months = models.IntegerField(help_text="Number of months to repay")
    interest_rate = models.DecimalField(max_digits=5, decimal_places=3, default=0.003, 
                                        help_text="Monthly interest rate (e.g., 0.003 for 0.3%)")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, editable=False)
    status = models.CharField(max_length=10, choices=LOAN_STATUS_CHOICES, default='PENDING')
    date_applied = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Loan Application by {self.farmer} - {self.get_status_display()}"
    
    def calculate_interest(self):
        if self.amount_approved:
            total_repaid = self.repayments.aggregate(models.Sum('amount_paid'))['amount_paid__sum'] or 0
            outstanding = self.amount_approved - total_repaid
            return outstanding * self.interest_rate
        return 0
        
    def calculate_balance(self):
        # Only calculate if amount_approved exists
        if self.amount_approved:
            total_repaid = self.repayments.aggregate(models.Sum('amount_paid'))['amount_paid__sum'] or 0
            interest = self.calculate_interest()
            return self.amount_approved + interest - total_repaid
        return 0
    
    def save(self, *args, **kwargs):
        # For new instances, set balance to amount_approved or 0
        if not self.pk:
            self.balance = self.amount_approved or 0
        else:
            # For existing instances, calculate the balance
            self.balance = self.calculate_balance()
        super().save(*args, **kwargs)

class LoanRepayment(models.Model):
    loan = models.ForeignKey(LoanApplication, on_delete=models.CASCADE, related_name='repayments')
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, help_text="Bank Transfer, Mobile Money, etc.")
    
    def __str__(self):
        return f"Repayment of {self.amount_paid} for Loan {self.loan.id}"
    
    def save(self, *args, **kwargs):
        # First save the repayment
        super().save(*args, **kwargs)
        # Then update the loan balance
        self.loan.balance = self.loan.calculate_balance()
        self.loan.save(update_fields=['balance'])