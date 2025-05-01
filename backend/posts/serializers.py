from rest_framework import serializers
from .models import Post, Comment

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'content', 'created_at']
        extra_kwargs = {
            'created_at': {'read_only': True}
        }

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_at']
        extra_kwargs = {
            'created_at': {'read_only': True}
        }
    
    def create(self, validated_data):
        validated_data.update({
            'user': self.context['request'].user,
            # 'post_id': self.context['view'].kwargs['post_pk'], <-- stopped working
        })
        return super().create(validated_data)