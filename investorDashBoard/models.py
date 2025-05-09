from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.conf import settings
from farmerDashBoard.models import FarmingSeason


class Investment(models.Model):
    INVESTMENT_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('ACTIVE', 'Active'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    investor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='investments')
    farming_season = models.ForeignKey(FarmingSeason, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date_invested = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=22, choices=INVESTMENT_STATUS_CHOICES, default='PENDING')
    expected_return = models.DecimalField(max_digits=12, decimal_places=2)
    actual_return = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('investor', 'farming_season')
    
    def __str__(self):
        return f"${self.amount} invested by {self.investor} in {self.farming_season}"
    
    def __repr__(self):
        return f"Investment(id={self.id}, investor={self.investor}, farming_season={self.farming_season})"


class MarketTrend(models.Model):
    TREND_TYPE_CHOICES = (
        ('PRICE', 'Price'),
        ('DEMAND', 'Demand'),
        ('SUPPLY', 'Supply'),
    )
    
    CROP_TYPE_CHOICES = (
        ('CORN', 'Corn'),
        ('SOYBEANS', 'Soybeans'),
        ('WHEAT', 'Wheat'),
    )
    
    crop_type = models.CharField(max_length=10, choices=CROP_TYPE_CHOICES)
    region = models.CharField(max_length=100)
    trend_type = models.CharField(max_length=10, choices=TREND_TYPE_CHOICES)
    trend_value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('crop_type', 'region', 'trend_type', 'date')
    
    def __str__(self):
        return f"{self.get_trend_type_display()} trend for {self.get_crop_type_display()} in {self.region} on {self.date}"
    
    def __repr__(self):
        return f"MarketTrend(id={self.id}, crop_type={self.crop_type}, region={self.region}, trend_type={self.trend_type})"