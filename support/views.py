from django.shortcuts import render

# Create your views here.
class SupportTicketViewSet(viewsets.ModelViewSet):
    """
    API endpoint for support tickets
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    serializer_class = SupportTicketSerializer
    
    def get_queryset(self):
        return SupportTicket.objects.filter(user=self.request.user).order_by('-date_created')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FarmingGuideViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for farming guides (read-only)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FarmingGuideSerializer
    queryset = FarmingGuide.objects.all().order_by('-date_created')
    
    @action(detail=False, methods=['get'])
    def by_crop(self, request):
        crop_type = request.query_params.get('crop_type', None)
        
        if crop_type:
            guides = FarmingGuide.objects.filter(crop_type=crop_type).order_by('-date_created')
        else:
            guides = FarmingGuide.objects.all().order_by('-date_created')
        
        serializer = FarmingGuideSerializer(guides, many=True)
        return Response(serializer.data)


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for FAQs (read-only)
    """
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FAQSerializer
    queryset = FAQ.objects.all()
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        category = request.query_params.get('category', None)
        
        if category:
            faqs = FAQ.objects.filter(category=category)
        else:
            faqs = FAQ.objects.all()
        
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data)
