from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Count, Q
from django.utils import timezone
from decimal import Decimal


from django.db.models import Sum

ZERO_DECIMAL = Decimal('0.00')


from .models import (
    Farm, Crop, FarmingSeason, 
    Payout, WeatherForecast, MarketTrend, 
    )
from investorDashBoard.models import Investment
from .serializers import (
    FarmSerializer, CropSerializer, FarmingSeasonSerializer,
    PayoutSerializer, WeatherForecastSerializer,
    MarketTrendSerializer,PayoutSerializer,DashboardOverviewSerializer
)
from investorDashBoard.serializers import InvestmentSerializer
from .permissions import IsFarmer, IsOwnerOrReadOnly

def get_queryset(self):
    if not self.request.user.is_authenticated:
        return self.model.objects.none()  # Return empty queryset for anonymous users
    return super().get_queryset()

class FarmerDashboardView(APIView):
    """
    API view for the farmer dashboard overview
    """
    permission_classes = [permissions.IsAuthenticated, IsFarmer, IsOwnerOrReadOnly]
    
    def get(self, request):
        user = request.user
        
        # Get total investments received
        total_investments = Investment.objects.filter(
            farming_season__farmer=user,
            status__in=['APPROVED', 'ACTIVE', 'COMPLETED']
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        # Get active farming seasons
        active_seasons = FarmingSeason.objects.filter(
            farmer=user,
            is_active=True
        )
        
        # Get pending payouts
        pending_payouts = Payout.objects.filter(
            farmer=user,
            status__in=['PENDING', 'APPROVED', 'PROCESSING']
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        # Calculate withdrawable earnings
        completed_investments = Investment.objects.filter(
            farming_season__farmer=user,
            status='COMPLETED'
        )
        
        withdrawable_earnings = Decimal('0.00')
        for investment in completed_investments:
            if investment.actual_return:
                withdrawable_earnings += investment.actual_return
        
        # Subtract already requested payouts
        processed_payouts = Payout.objects.filter(
            farmer=user,
            status__in=['PENDING', 'APPROVED', 'PROCESSING', 'COMPLETED']
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
        
        withdrawable_earnings -= processed_payouts
        withdrawable_earnings = max(Decimal('0.00'), withdrawable_earnings)
        
        # Get recent activities
        recent_investments = Investment.objects.filter(
            farming_season__farmer=user
        ).order_by('-date_invested')[:5]
        
        recent_payouts = Payout.objects.filter(
            farmer=user
        ).order_by('-date_requested')[:5]
        
        # Prepare data for serialization
        data = {
            'total_investments': total_investments,
            'active_seasons_count': active_seasons.count(),
            'pending_payouts': pending_payouts,
            'withdrawable_earnings': withdrawable_earnings,
            'recent_investments': recent_investments,
            'recent_payouts': recent_payouts,
            'active_seasons': active_seasons[:5]  # Show only 5 most recent
        }
        
        serializer = DashboardOverviewSerializer(data)
        return Response(serializer.data)


class FarmViewSet(viewsets.ModelViewSet):
    """
    API endpoint for farms
    """
    permission_classes = [permissions.IsAuthenticated, IsFarmer, IsOwnerOrReadOnly]
    serializer_class = FarmSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Farm.objects.filter(farmer=self.request.user)
        else:
            return Farm.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)
    
    @action(detail=True, methods=['get'])
    def crops(self, request, pk=None):
        farm = self.get_object()
        crops = Crop.objects.filter(farm=farm)
        serializer = CropSerializer(crops, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def weather(self, request, pk=None):
        farm = self.get_object()
        forecasts = WeatherForecast.objects.filter(
            farm=farm,
            date__gte=timezone.now().date()
        ).order_by('date')
        serializer = WeatherForecastSerializer(forecasts, many=True)
        return Response(serializer.data)


class CropViewSet(viewsets.ModelViewSet):
    """
    API endpoint for crops
    """
    permission_classes = [permissions.IsAuthenticated, IsFarmer]
    serializer_class = CropSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Crop.objects.filter(farm__farmer=self.request.user)
        else:
            return Crop.objects.none()
    
    def perform_create(self, serializer):
        farm_id = self.request.data.get('farm')
        farm = Farm.objects.get(id=farm_id)
        
        if farm.farmer != self.request.user:
            return Response(
                {"detail": "You don't have permission to add crops to this farm."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer.save()


class FarmingSeasonViewSet(viewsets.ModelViewSet):
    """
    API endpoint for farming seasons
    """
    permission_classes = [permissions.IsAuthenticated, IsFarmer, IsOwnerOrReadOnly]
    serializer_class = FarmingSeasonSerializer
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return FarmingSeason.objects.filter(farmer=self.request.user)
        else:
            return FarmingSeason.objects.none()
    
    def perform_create(self, serializer):
        serializer.save(farmer=self.request.user)
    
    @action(detail=True, methods=['get'])
    def investments(self, request, pk=None):
        season = self.get_object()
        investments = Investment.objects.filter(farming_season=season)
        serializer = InvestmentSerializer(investments, many=True)
        return Response(serializer.data)




class FinancialsView(APIView):
    """
    API view for financial information
    """
    permission_classes = [permissions.IsAuthenticated, IsFarmer]
    
    def get(self, request):
        user = request.user
        
        # Get investments by status
        investments = Investment.objects.filter(
            farming_season__farmer=user
        )
        
        investment_summary = {
            'total_investments': investments.aggregate(total=Sum('amount'))['total'] or ZERO_DECIMAL,
            'active_investments': investments.filter(status='ACTIVE').aggregate(total=Sum('amount'))['total'] or ZERO_DECIMAL,
            'completed_investments': investments.filter(status='COMPLETED').aggregate(total=Sum('amount'))['total'] or ZERO_DECIMAL,
        }
        
        # Calculate withdrawable earnings
        completed_investments = investments.filter(status='COMPLETED')
        withdrawable_earnings = completed_investments.aggregate(total=Sum('actual_return'))['total'] or ZERO_DECIMAL
        
        # Subtract already requested payouts
        processed_payouts = Payout.objects.filter(
            farmer=user,
            status__in=['PENDING', 'APPROVED', 'PROCESSING', 'COMPLETED']
        ).aggregate(total=Sum('amount'))['total'] or ZERO_DECIMAL
        
        withdrawable_earnings -= processed_payouts
        withdrawable_earnings = max(ZERO_DECIMAL, withdrawable_earnings)
        
        # Get payout history
        payouts = Payout.objects.filter(farmer=user).order_by('-date_requested')
        
        # Prepare data for serialization
        data = {
            'total_investments': investment_summary['total_investments'],
            'active_investments': investment_summary['active_investments'],
            'completed_investments': investment_summary['completed_investments'],
            'withdrawable_earnings': withdrawable_earnings,
            'payouts': PayoutSerializer(payouts, many=True).data
        }
        
        return Response(data)

class PayoutRequestView(APIView):
    """
    API view for requesting payouts
    """
    permission_classes = [permissions.IsAuthenticated, IsFarmer]
    
    def post(self, request):
        serializer = PayoutRequestSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            amount = serializer.validated_data['amount']
            
            # Calculate withdrawable earnings
            completed_investments = Investment.objects.filter(
                farming_season__farmer=user,
                status='COMPLETED'
            )
            
            withdrawable_earnings = Decimal('0.00')
            for investment in completed_investments:
                if investment.actual_return:
                    withdrawable_earnings += investment.actual_return
            
            # Subtract already requested payouts
            processed_payouts = Payout.objects.filter(
                farmer=user,
                status__in=['PENDING', 'APPROVED', 'PROCESSING', 'COMPLETED']
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')
            
            withdrawable_earnings -= processed_payouts
            withdrawable_earnings = max(Decimal('0.00'), withdrawable_earnings)
            
            if amount > withdrawable_earnings:
                return Response(
                    {"detail": "You cannot request more than your withdrawable earnings."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            payout = Payout(
                farmer=user,
                amount=amount,
                status='PENDING',
                notes=serializer.validated_data.get('notes', '')
            )
            payout.save()
            
            return Response(
                {"detail": f"Payout request for ${amount} has been submitted successfully."},
                status=status.HTTP_201_CREATED
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PayoutViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing payouts (read-only)
    """
    permission_classes = [permissions.IsAuthenticated, IsFarmer]
    serializer_class = PayoutSerializer
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Payout.objects.none()
        return Payout.objects.filter(farmer=self.request.user).order_by('-date_requested')


class MarketTrendViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing market trends (read-only)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MarketTrendSerializer
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return MarketTrend.objects.none()
        
        user = self.request.user
        if hasattr(user, 'account_type') and user.account_type == 'FARMER':
            # Get crop types for the farmer's farms
            farms = Farm.objects.filter(farmer=user)
            crop_types = Crop.objects.filter(
                farm__in=farms
            ).values_list('type', flat=True).distinct()
            
            return MarketTrend.objects.filter(
                crop_type__in=crop_types,
                date__gte=timezone.now().date() - timezone.timedelta(days=30)
            ).order_by('crop_type', 'region', '-date')
        
        return MarketTrend.objects.filter(
            date__gte=timezone.now().date() - timezone.timedelta(days=30)
        ).order_by('crop_type', 'region', '-date')


