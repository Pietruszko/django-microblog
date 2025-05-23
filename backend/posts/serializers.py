from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source='user.userprofile.first_name', read_only=True)
    user_avatar = serializers.ImageField(source='user.userprofile.avatar', read_only=True)
    user_id = serializers.IntegerField(source='user.userprofile.id', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'content', 'created_at', 'user_first_name', 'user_avatar', 'user_id']
        extra_kwargs = {
            'created_at': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
class CommentSerializer(serializers.ModelSerializer):
    user_first_name = serializers.CharField(source='user.userprofile.first_name', read_only=True)
    user_avatar = serializers.ImageField(source='user.userprofile.avatar', read_only=True)
    user_id = serializers.IntegerField(source='user.userprofile.id', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at', 'user_first_name', 'user_avatar', 'user_id']
        extra_kwargs = {
            'created_at': {'read_only': True}
        }
    
    def create(self, validated_data):
        validated_data.update({
            'user': self.context['request'].user,
            # 'post_id': self.context['view'].kwargs['post_pk'], <-- stopped working
        })
        return super().create(validated_data)