from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    bio = serializers.CharField(required=False, allow_blank=True)
    avatar = serializers.ImageField(required=False)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        UserProfile.objects.create(
            user=user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            bio=validated_data.get('bio', 'This is my profile!'),
            avatar=validated_data.get('avatar', None),
        )
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user_id', 'first_name', 'last_name', 'bio', 'avatar']
        extra_kwargs = {
            'bio': {'required': False, 'allow_blank': True},
            'avatar': {'required': False}
        }

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['user_id'] = self.user.id

        return data