from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Profile, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'other_name', 'gender', 'phone_number',
                  'email', 'address', 'account_type', 'national_id', 'date_joined', 'is_active', 'is_staff', 'is_superuser', 'date_joined']

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['account_type'] = user.account_type
        token['phone_number'] = user.phone_number
        token['username'] = user.username
        token['user_id'] = user.id
        
        # Convert datetime to string
        token['date_joined'] = user.date_joined.isoformat() if user.date_joined else None
        
        # Check if profile and profile_picture exist before accessing
        try:
            profile_picture = user.profile.profile_picture.url if user.profile.profile_picture else None
            token['profile_picture'] = profile_picture
        except (AttributeError, ValueError):
            token['profile_picture'] = None
            
        return token

class ResterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ['email', 'username', 'account_type', 'password', 'password2']
    
    def validate(self, attrs):
        """
        Checks if the two passwords match
        Args:
        attrs (dict): containing email, username, password, password2
        Raises:
        serializers.ValidationError: if passwords do not match
        Returns:
        dict: validated attrs
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields does not match"}
            )
        return attrs
    
    def create(self, validated_data):
        """
        Creates a new user
        Args:
        validated_data (dict): containing email, username, password
        Returns:
        User: created user
        """
        # Remove password2 as it's not needed for creating the user
        validated_data.pop('password2', None)
        
        user = User.objects.create_user(
            email=validated_data['email'],
            account_type = validated_data['account_type'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        # No need to set_password again as create_user already hashes the password
        return user