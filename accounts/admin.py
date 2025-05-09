from django.contrib import admin
from .models import User, Profile

# Inline Admin Class
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fields = ('profile_type', 'profile_picture', 'bio', 'date_of_birth', 'residential_address')
    readonly_fields = ('user',)

# Map account types to inlines
account_type_inlines = {
    'INVESTOR': ('investment_amount', 'preferred_return_type', 'preferred_payment_method'),
    'FARMER': ('farming_type', 'main_crops_livestock', 'farm_size'),
    'AGENT': ('specialization', 'areas_covered', 'commission_rate'),
}

# Main User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username', 
        'email', 
        'account_type', 
        'is_active',
        'date_joined'
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (
        'account_type', 
        'is_active',
        'is_staff',
        'date_joined'
    )
    date_hierarchy = 'date_joined'
    ordering = ('-date_joined',)
    readonly_fields = ('date_joined', 'last_login')
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': (
            'first_name', 
            'last_name', 
            'other_name',
            'email', 
            'gender', 
            'phone_number',
            'address',
            'national_id',
            'account_type'
        )}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions'
        )}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    def get_inline_instances(self, request, obj=None):
        """Only show relevant profile inline based on account_type"""
        if not obj:
            return []
            
        profile_inlines = []
        if obj.account_type in account_type_inlines:
            profile_inlines.append(ProfileInline)
            
        return [inline(self.model, self.admin_site) for inline in profile_inlines]

# Standalone Profile Admin (optional)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'profile_type',
    )
    search_fields = ('user__username', 'user__email')
    list_filter = ('profile_type',)
    readonly_fields = ('user',)
    raw_id_fields = ('user',)