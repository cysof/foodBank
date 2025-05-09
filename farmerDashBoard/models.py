from django.db import models
from django.utils import timezone
from decimal import Decimal
from django.conf import settings

class Farm(models.Model):
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farms')
    farm_name = models.CharField(max_length=255, help_text="Rice Farm")
    location = models.CharField(max_length=255)
    farm_size = models.DecimalField(max_digits=10, decimal_places=2, help_text='Size in acres')
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.farm_name
    
    @property
    def total_crop(self):
        return self.crops.count()
    
    @property
    def active_crops(self):
        return self.crops.filter(season__is_active=True).count()
    
class Crop(models.Model):
    CROP_TYPE_CHOICE = (
        ('MAIZE', 'Maize'),
        ('WHEAT', 'Wheat'),
        ('RICE', 'Rice'),
        ('BEANS', 'Beans'),
    )
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crops')
    crop_type = models.CharField(max_length=20, choices=CROP_TYPE_CHOICE)
    variety = models.CharField(max_length=100, null=True, blank=True)
    area_square = models.DecimalField(max_digits=10, decimal_places=2, help_text='Area in Acres')
    date_added = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """Return a string representation of the Crop object displaying the crop type, variety, and farm name."""
        return f"{self.get_crop_type_display()} ({self.variety}) at {self.farm.farm_name}"

class FarmingSeason(models.Model):
    SEASON_STATU_CHOICES = (
        ('PLANNING', 'Planning'),
        ('PLANTING', 'Planting'),
        ('GROWING', 'Growing'),
        ('HARVESTING', 'Harvesting'),
        ('COMPLETED', 'Completed'),
    )
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='farming_seasons')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='seasons')
    name = models.CharField(max_length=255)
    start_date = models.DateField()
    expected_end_date = models.DateField()
    actual_end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=SEASON_STATU_CHOICES , default='PLANNING')
    total_investment_received = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    expected_yield = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    actual_yield = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name}  -  {self.crop}"
    
    
    @property
    def progress_percentage(self):
        """Calculating and returning the progress percentage of the farming season"""
        if self.status == 'COMPLETED':
            return 100
        if self.status == 'PLANNING':
            return 10
        
        if not self.start_date or not self.expected_end_date:
            return 0
        total_days = (self.expected_end_date - self.start_date).days
        if total_days <= 0:
            return 0
        
        days_passed = (timezone.now() - self.start_date).days
        percentage = min(100, max(0, (days_passed / total_days) * 100))
        
        if self.status == 'PLANTING':
            return min(percentage, 25)
        elif self.status == 'GROWING':
            return min(25 + percentage * 0.5, 75)
        elif self.status == 'HARVESTING':
            return min(75 + percentage * 0.25, 95)
            
        return percentage
    
    
    
class Payout(models.Model):
    PAYOUT_STATUS_CHOICES = (
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
    )
    
    farmer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payouts')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date_requested   = models.DateTimeField(auto_now_add=True)
    date_processed = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=PAYOUT_STATUS_CHOICES, default='PENDING')
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"${self.amount} payout to {self.farmer} - {self.get_status_display()}"
    
    
    
class WeatherForecast(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='weather_forecasts')
    date = models.DateField()
    temperature_high = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_low = models.DecimalField(max_digits=5, decimal_places=2)
    precipitation = models.DecimalField(max_digits=5, decimal_places=2, help_text="Precipitation in mm")
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    humidity = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        unique_together = ('farm', 'date')
    
    def __str__(self):
        return f"Weather for {self.farm.farm_name} on {self.date}"
    

class MarketTrend(models.Model):
    TREND_TYPE_CHOICES = (
        ('PRICE', 'Price'),
        ('DEMAND', 'Demand'),
        ('SUPPLY', 'Supply'),
    )
    
    crop_type = models.CharField(max_length=20)
    region = models.CharField(max_length=100)
    trend_type = models.CharField(max_length=10, choices=TREND_TYPE_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    
    class Meta:
        unique_together = ('crop_type', 'region', 'trend_type', 'date')
    
    def __str__(self):
        return f"{self.get_trend_type_display()} trend for {self.crop_type} in {self.region} on {self.date}"

    
    
    
    