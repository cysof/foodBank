from rest_framework import serializers
from .models import Farm, Crop, FarmingSeason, Payout, WeatherForecast, MarketTrend
from django.contrib.auth import get_user_model
from investorDashBoard.serializers import InvestmentSerializer

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'account_type']


class FarmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farm
        fields = ['id', 'farmer', 'farm_name', 'location', 'farm_size', 'description', ]

class CropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crop
        fields = ['id', 'farm', 'crop_type', 'variety', 'area_square', 'date_added']

class FarmingSeasonSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmingSeason
        fields = ['id', 'farmer', 'crop', 'name', 'start_date', 'expected_end_date', 'actual_end_date', 'status', 'total_investment_received', 'expected_yield', 'actual_yield', 'is_active']

class PayoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payout
        fields = ['id', 'farmer', 'amount', 'date_requested', 'date_processed', 'status', 'notes']

class WeatherForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherForecast
        fields = ['id', 'farm', 'date', 'temperature_high', 'temperature_low', 'precipitation', 'wind_speed', 'humidity']

class MarketTrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketTrend
        fields = ['id', 'crop_type', 'region', 'trend_type', 'value', 'date']

class DashboardOverviewSerializer(serializers.Serializer):
    total_investments = serializers.DecimalField(max_digits=12, decimal_places=2)
    active_seasons_count = serializers.IntegerField()
    pending_payouts = serializers.DecimalField(max_digits=12, decimal_places=2)
    withdrawable_earnings = serializers.DecimalField(max_digits=12, decimal_places=2)
    recent_investments = serializers.SerializerMethodField()
    recent_payouts = serializers.SerializerMethodField()
    active_seasons = serializers.SerializerMethodField()

    def get_recent_investments(self, obj):
        return InvestmentSerializer(obj['recent_investments'], many=True).data

    def get_recent_payouts(self, obj):
        return PayoutSerializer(obj['recent_payouts'], many=True).data

    def get_active_seasons(self, obj):
        return FarmingSeasonSerializer(obj['active_seasons'], many=True).data

class FinancialsSummarySerializer(serializers.Serializer):
    total_investments = serializers.DecimalField(max_digits=12, decimal_places=2)
    active_investments = serializers.DecimalField(max_digits=12, decimal_places=2)
    completed_investments = serializers.DecimalField(max_digits=12, decimal_places=2)
    withdrawable_earnings = serializers.DecimalField(max_digits=12, decimal_places=2)
    payouts = PayoutSerializer(many=True)