from django.contrib import admin
from .models import (Farm,
                     Crop, 
                     FarmingSeason,
                     Payout, 
                     WeatherForecast,
                     MarketTrend,
                     )

@admin.register(Farm)
class UserAdmin(admin.ModelAdmin):
    list_display = (
       'farmer',
       'farm_name',
       'location',
       'farm_size'
    )
    search_fields = ('farm_name', 'location', 'farm_size', 'farmer')
    list_filter = (
        'farm_name', 
        'farm_size',
    )
admin.site.register(Crop)
admin.site.register(Payout)
admin.site.register(WeatherForecast)
admin.site.register(MarketTrend)
admin.site.register(FarmingSeason)
    