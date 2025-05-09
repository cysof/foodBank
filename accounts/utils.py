from drf_yasg.inspectors import SwaggerAutoSchema

class SafeSwaggerAutoSchema(SwaggerAutoSchema):
    """Custom schema generator that handles anonymous users safely."""
    
    def get_queryset(self):
        """Handle cases where queryset access might fail with anonymous users."""
        try:
            return super().get_queryset()
        except Exception:
            return None
            
    def get_filter_parameters(self):
        """Handle filter parameter generation safely."""
        try:
            return super().get_filter_parameters()
        except Exception:
            return []