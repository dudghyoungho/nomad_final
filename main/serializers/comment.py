from rest_framework import serializers
from ..models.comment import Comment

class CommentSerializer(serializers.ModelSerializer):
    # author_name은 기본적으로 "익명"으로 설정
    author_name = serializers.CharField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'content', 'is_private', 'created_at', 'parent']
        ref_name = 'CommentSerializer'  # ref_name 명시적으로 설정
