# serializers.py
from rest_framework import serializers
from ..models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['author_name', 'content', 'created_at']
        ref_name = 'PostWithCommentSerializer_Comment'  # ref_name을 달리 설정

class PostWithCommentsSerializer(serializers.ModelSerializer):
    # 댓글을 가져올 때 평평하게 반환하기 위한 설정
    comments = CommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ['id', 'author_name', 'title', 'content', 'created_at', 'comments']

    def to_representation(self, instance):
        """
        댓글과 대댓글을 평평하게 반환하기 위한 처리
        """
        data = super().to_representation(instance)

        # 댓글은 평평하게 만들기 위해 리스트로 반환
        comments = data.pop('comments', [])
        flat_comments = []

        # 댓글 및 대댓글을 한 리스트로 합침
        for comment in comments:
            flat_comments.append(comment)

        data['comments'] = flat_comments
        return data
