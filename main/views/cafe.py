from django.db.models.functions import ACos, Cos, Radians, Sin
from django.db.models import F, FloatField, ExpressionWrapper
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from drf_yasg.utils import swagger_auto_schema
from rest_framework.exceptions import NotFound
from drf_yasg import openapi
from ..models.cafe import Cafe
from ..models.profile import Profile
from ..serializers.cafe import CafeSerializer
from ..services import NaverMapService
from django.http import JsonResponse


# 주변 카페 목록 조회
from django.db.models import FloatField, ExpressionWrapper

class NearbyCafeListView(APIView):
    """
    현재 위치를 기반으로 가까운 카페 반환
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="주변 카페 목록",
        operation_description="사용자의 현재 위치를 기반으로 가까운 카페를 반환합니다.",
        manual_parameters=[
            openapi.Parameter('latitude', openapi.IN_QUERY, description="사용자 위도", type=openapi.TYPE_NUMBER),
            openapi.Parameter('longitude', openapi.IN_QUERY, description="사용자 경도", type=openapi.TYPE_NUMBER),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description="카페 이름"),
                        'address': openapi.Schema(type=openapi.TYPE_STRING, description="카페 주소"),
                        'opening_hours': openapi.Schema(type=openapi.TYPE_STRING, description="영업 시간"),
                        'is_open': openapi.Schema(type=openapi.TYPE_STRING, description="영업 상태"),
                        'cal_distance': openapi.Schema(type=openapi.TYPE_NUMBER, description="사용자와 카페 간 거리 (km)"),
                    },
                ),
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="오류 메시지"),
                },
            ),
        }
    )
    def get(self, request, *args, **kwargs):
        user_lat = request.query_params.get("latitude")
        user_lon = request.query_params.get("longitude")

        if not user_lat or not user_lon:
            return Response({"error": "latitude와 longitude가 필요합니다."}, status=400)

        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)
        except ValueError:
            return Response({"error": "latitude와 longitude는 숫자여야 합니다."}, status=400)

        # Annotate cafes with distance and order them
        cafes = Cafe.objects.annotate(
            calculated_distance=ExpressionWrapper(
                6371 * ACos(
                    Cos(Radians(F("latitude"))) * Cos(Radians(user_lat)) *
                    Cos(Radians(F("longitude")) - Radians(user_lon)) +
                    Sin(Radians(F("latitude"))) * Sin(Radians(user_lat))
                ),
                output_field=FloatField()
            )
        ).order_by("calculated_distance")[:5]

        serializer = CafeSerializer(cafes, many=True)
        return Response(serializer.data, status=200)

class MidpointCafeListView(APIView):
    """
    두 사용자의 중간 지점에서 가장 가까운 카페 5개를 반환합니다.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="중간 지점 근처 카페 목록",
        operation_description="사용자 1의 현재 위치를 받아 고정된 사용자 2의 위치와의 중간 지점에서 가장 가까운 카페 5개를 반환합니다.",
        manual_parameters=[
            openapi.Parameter(
                'user1_latitude', openapi.IN_QUERY, description="사용자 1의 위도", type=openapi.TYPE_NUMBER, required=True
            ),
            openapi.Parameter(
                'user1_longitude', openapi.IN_QUERY, description="사용자 1의 경도", type=openapi.TYPE_NUMBER, required=True
            ),
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'name': openapi.Schema(type=openapi.TYPE_STRING, description="카페 이름"),
                        'address': openapi.Schema(type=openapi.TYPE_STRING, description="카페 주소"),
                        'latitude': openapi.Schema(type=openapi.TYPE_NUMBER, description="카페 위도"),
                        'longitude': openapi.Schema(type=openapi.TYPE_NUMBER, description="카페 경도"),
                        'distance': openapi.Schema(type=openapi.TYPE_NUMBER, description="중간 지점으로부터의 거리 (km)"),
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description="카페 상태 (예: 영업 중)"),
                    }
                )
            ),
            400: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description="에러 메시지")
                }
            )
        }
    )
    def get(self, request, *args, **kwargs):
        # 사용자 1의 좌표 가져오기
        user1_lat = request.query_params.get("user1_latitude", None)
        user1_lon = request.query_params.get("user1_longitude", None)

        # 고정된 사용자 2의 좌표
        user2_lat = 37.556661  # 예: 서울의 위도
        user2_lon = 126.9057804  # 예: 서울의 경도

        # 좌표 유효성 검사
        if not all([user1_lat, user1_lon]):
            raise ValidationError({
                "error": "user1_latitude와 user1_longitude는 필수 쿼리 파라미터입니다."
            })

        try:
            user1_lat = float(user1_lat)
            user1_lon = float(user1_lon)
        except ValueError:
            raise ValidationError({"error": "모든 좌표 값은 숫자여야 합니다."})

        # 중간 지점 계산
        mid_lat = (user1_lat + user2_lat) / 2
        mid_lon = (user1_lon + user2_lon) / 2

        # 중간 지점에서 가까운 카페 조회
        cafes = Cafe.objects.annotate(
            calculated_distance=ExpressionWrapper(
                6371 * ACos(
                    Cos(Radians(F("latitude"))) * Cos(Radians(mid_lat)) *
                    Cos(Radians(F("longitude")) - Radians(mid_lon)) +
                    Sin(Radians(F("latitude"))) * Sin(Radians(mid_lat))
                ),
                output_field=FloatField()
            )
        ).filter(calculated_distance__lte=5.0).order_by("calculated_distance")[:5]  # 5km 이내 상위 5개

        # 카페 데이터를 직렬화하여 응답 반환
        serializer = CafeSerializer(cafes, many=True)
        return Response(serializer.data)



# 카페 상세 조회
class NearbyCafeDetailView(RetrieveUpdateDestroyAPIView):
    """
    특정 카페의 상세 정보 제공.
    """
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="카페 상세 정보 조회",
        operation_description="특정 카페의 상세 정보를 조회합니다 (cafe_name으로 조회).",
        responses={200: CafeSerializer(), 404: "카페를 찾을 수 없습니다."}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_object(self):
        """
        cafe_name을 기준으로 객체를 가져옵니다.
        """
        cafe_name = self.kwargs.get("cafe_name")
        if not cafe_name:
            raise NotFound(detail="카페 이름이 제공되지 않았습니다.")

        try:
            return Cafe.objects.get(name=cafe_name)
        except Cafe.DoesNotExist:
            raise NotFound(detail="해당 이름의 카페를 찾을 수 없습니다.")