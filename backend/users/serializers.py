from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from posts.models import Post

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
        profile = UserProfile.objects.create(
            user=user,
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            bio=validated_data.get('bio', 'This is my profile!'),
        )
        if 'avatar' in validated_data:
            profile.avatar = validated_data['avatar']
            profile.save()
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id')
    avatar = serializers.ImageField(required=False)
    posts = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id', 'user_id', 'first_name', 'last_name', 'bio', 'avatar', 'posts']
    
    def get_posts(self, obj):
        posts = Post.objects.filter(user=obj.user).order_by('-created_at')[:5]
        return [
            {
                'id': post.id,
                'content': post.content,
                'created_at': post.created_at
            } for post in posts
        ]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data['user_id'] = self.user.id

        return data