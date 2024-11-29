from rest_framework import serializers
from ..models.review import Review

class ReviewSerializer(serializers.ModelSerializer):
    cafe = serializers.SerializerMethodField()  # 카페 이름 반환

    class Meta:
        model = Review
        fields = ['cafe', 'content', 'created_at']  # 필요한 필드만 포함

    def get_cafe(self, obj):
        """
        카페 이름 반환
        """
        return obj.cafe.name  # 카페 이름만 반환
