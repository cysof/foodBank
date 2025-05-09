from rest_framework import serializers
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal

from .models import Investment
from django.contrib.auth import get_user_model

User = get_user_model()


class InvestmentSerializer(serializers.ModelSerializer):
    investor_name = serializers.SerializerMethodField(source='investor')
    farming_season_name = serializers.SerializerMethodField(source='farming_season.name')
    
    class Meta:
        model = Investment
        fields = ['id', 'investor', 'investor_name', 'farming_season', 'farming_season_name', 
                  'amount', 'date_invested', 'status', 'expected_return', 'actual_return']
    
    def get_investor_name(self, obj):
        return str(obj.investor)
    
    def get_farming_season_name(self, obj):
        return obj.farming_season.name