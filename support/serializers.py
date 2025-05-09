from rest_framework import serializers
from django.db.models import Sum
from django.utils import timezone
from decimal import Decimal
from investorDashBoard.serializers import InvestmentSerializer
from farmerDashBoard.serializers import PayoutSerializer, FarmingSeasonSerializer

from .models import SupportTicket, FarmingGuide, FAQ
from django.contrib.auth import get_user_model

User = get_user_model()



class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = ['id', 'user', 'subject', 'description', 'status', 'priority', 
                  'date_created', 'date_updated']


class FarmingGuideSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()
    
    class Meta:
        model = FarmingGuide
        fields = ['id', 'title', 'content', 'crop_type', 'author', 'author_name', 
                  'date_created', 'date_updated']
    
    def get_author_name(self, obj):
        if obj.author:
            return f"{obj.author.first_name} {obj.author.last_name}"
        return "Unknown"


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'category', 'order']


class DashboardOverviewSerializer(serializers.Serializer):
    total_investments = serializers.DecimalField(max_digits=12, decimal_places=2)
    active_seasons_count = serializers.IntegerField()
    pending_payouts = serializers.DecimalField(max_digits=12, decimal_places=2)
    withdrawable_earnings = serializers.DecimalField(max_digits=12, decimal_places=2)
    recent_investments = InvestmentSerializer(many=True)
    recent_payouts = PayoutSerializer(many=True)
    active_seasons = FarmingSeasonSerializer(many=True)


class FinancialsSummarySerializer(serializers.Serializer):
    total_investments = serializers.DecimalField(max_digits=12, decimal_places=2)
    active_investments = serializers.DecimalField(max_digits=12, decimal_places=2)
    completed_investments = serializers.DecimalField(max_digits=12, decimal_places=2)
    withdrawable_earnings = serializers.DecimalField(max_digits=12, decimal_places=2)
    payouts = PayoutSerializer(many=True)
