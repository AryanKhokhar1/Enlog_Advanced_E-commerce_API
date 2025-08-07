from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, UserProfile

class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password_confirm', 'phone', 'address')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Password fields didn't match.")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for user profile"""
    avatar = serializers.URLField(required=False)
    preferences = serializers.JSONField(required=False)
    
    class Meta:
        model = UserProfile
        fields = ('avatar', 'preferences', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user data"""
    profile = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'phone', 'address', 'date_of_birth', 'profile')
        read_only_fields = ('id', 'email')

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating user profile"""
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'address', 'date_of_birth', 'profile')
    
    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        
        # Update user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        # Update profile fields
        if profile_data:
            profile = instance.profile
            for attr, value in profile_data.items():
                setattr(profile, attr, value)
            profile.save()
        
        return instance