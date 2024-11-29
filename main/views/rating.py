from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from ..models.cafe import Cafe
from ..models.rating import Rating
from ..serializers.rating import RatingSerializer
from rest_framework.permissions import AllowAny



class RatingListView(APIView):
    """
    특정 카페의 별점 추가 및 평균 별점 조회
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="별점 추가",
        operation_description="특정 카페에 별점을 추가합니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'rating': openapi.Schema(type=openapi.TYPE_INTEGER, description="별점 (1~5)"),
            },
            required=['rating']
        ),
        responses={201: openapi.Response(
            description="별점 추가 성공",
            schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                "message": openapi.Schema(type=openapi.TYPE_STRING, description="결과 메시지"),
                "rating": openapi.Schema(type=openapi.TYPE_OBJECT, description="추가된 별점 정보"),
                "average_rating": openapi.Schema(type=openapi.TYPE_NUMBER, description="카페의 평균 별점")
            })
        )}
    )
    def post(self, request, cafe_name, *args, **kwargs):
        try:
            cafe = Cafe.objects.get(name=cafe_name)
        except Cafe.DoesNotExist:
            print(f"Error: Cafe '{cafe_name}' does not exist.")
            return Response({"error": "해당 카페를 찾을 수 없습니다."}, status=404)

        rating_value = request.data.get('rating')
        if not rating_value or not (1 <= int(rating_value) <= 5):
            print("Error: Invalid 'rating' value.")
            return Response({"error": "별점은 1에서 5 사이여야 합니다."}, status=400)

        # 별점 추가 또는 업데이트
        try:
            rating, created = Rating.objects.update_or_create(
                user=request.user if request.user.is_authenticated else None,
                cafe=cafe,
                defaults={'rating': rating_value}
            )
        except Exception as e:
            print(f"Error while creating or updating rating: {e}")
            return Response({"error": "별점을 처리하는 중 오류가 발생했습니다."}, status=500)

        # 평균 별점 계산
        all_ratings = Rating.objects.filter(cafe=cafe)
        if all_ratings.exists():
            avg_rating = sum([int(r.rating) for r in all_ratings]) / all_ratings.count()
        else:
            avg_rating = 0

        cafe.rating = avg_rating
        cafe.save()

        # 응답 데이터 생성
        serializer = RatingSerializer(rating)
        return Response({
            "message": "별점 등록하기를 눌러주세요.",
            "rating": serializer.data,
            "average_rating": avg_rating
        }, status=201)


    @swagger_auto_schema(
        operation_summary="평균 별점 조회",
        operation_description="특정 카페의 평균 별점을 조회합니다.",
        responses={200: openapi.Response(
            description="평균 별점 조회 성공",
            schema=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'average_rating': openapi.Schema(type=openapi.TYPE_NUMBER, description="카페의 평균 별점")
            })
        )}
    )
    def get(self, request, cafe_name, *args, **kwargs):
        try:
            cafe = Cafe.objects.get(name=cafe_name)
        except Cafe.DoesNotExist:
            return Response({"error": "해당 카페를 찾을 수 없습니다."}, status=404)

        all_ratings = Rating.objects.filter(cafe=cafe)
        avg_rating = sum([int(r.rating) for r in all_ratings]) / all_ratings.count() if all_ratings.count() else 0
        return Response({"average_rating": avg_rating})


class RatingDetailView(RetrieveUpdateDestroyAPIView):
    """
    별점 수정 및 삭제
    """
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [AllowAny]

    def perform_update(self, serializer):
        serializer.save()
        self.update_average_rating(serializer.instance.cafe)

    def perform_destroy(self, instance):
        cafe = instance.cafe
        instance.delete()
        self.update_average_rating(cafe)

    def update_average_rating(self, cafe):
        all_ratings = Rating.objects.filter(cafe=cafe)
        avg_rating = sum([int(r.rating) for r in all_ratings]) / all_ratings.count() if all_ratings.exists() else 0
        cafe.rating = avg_rating
        cafe.save()