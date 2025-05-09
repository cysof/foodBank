from django.contrib import admin
from .models import Investment

class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'investor', 'farming_season', 'amount', 'status')
    list_filter = ('status', 'farming_season')
    search_fields = ('investor__username', 'farming_season__name')
    
admin.site.register(Investment, InvestmentAdmin)