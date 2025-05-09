from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .serializers import InvestmentSerializer
from .models import Investment

# Create your views here.



class InvestmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for viewing investments (read-only)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = InvestmentSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            if user.account_type == 'FARMER':
                
                return Investment.objects.filter(farming_season__farmer=user)
            else:
                return Investment.objects.filter(investor=user)
        else:
            return Investment.objects.none()