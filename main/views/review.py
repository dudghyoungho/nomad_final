from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from drf_yasg.utils import swagger_auto_schema
from ..models.cafe import Cafe
from ..models.review import Review
from ..serializers.review import ReviewSerializer


class ReviewListView(ListCreateAPIView):
    """
    특정 카페의 리뷰 조회 및 작성
    """
    serializer_class = ReviewSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="리뷰 조회 및 작성",
        operation_description="특정 카페의 리뷰를 조회하거나 새로운 리뷰를 작성합니다.",
        responses={200: ReviewSerializer(many=True), 201: ReviewSerializer()},
        request_body=ReviewSerializer
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        cafe_name = self.kwargs.get('cafe_name')
        return Review.objects.filter(cafe__name=cafe_name)

    def perform_create(self, serializer):
        cafe_name = self.kwargs.get('cafe_name')
        try:
            cafe = Cafe.objects.get(name=cafe_name)
        except Cafe.DoesNotExist:
            raise ValidationError({"cafe": "해당 카페를 찾을 수 없습니다."})

        # user 없이 저장
        serializer.save(cafe=cafe)


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    """
    특정 카페의 리뷰 수정 및 삭제
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
