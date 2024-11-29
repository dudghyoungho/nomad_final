from rest_framework import serializers
from ..models.post import Post

class PostSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(read_only=True)  # 여기에서 author_name을 read_only로 설정해줘야 perform_create에서 설정된 값을 그대로 사용합니다.

    class Meta:
        model = Post
        fields = ['id', 'author_name', 'title', 'content', 'created_at']
