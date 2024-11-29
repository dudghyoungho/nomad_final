"""
URL configuration for nomad_kor project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

# 인증 및 프로필 관련 뷰
from main.views.signup import SignupView
from main.views.login import LoginView
from main.views.logout import LogoutView
from main.views.profile import create_profile, ProfileDetailView, ProfileUpdateView

# 게시판 관련 뷰
from main.views.position import PositionListView, PositionDetailView
from main.views.ftf import FTFListView, FTFDetailView
from main.views.anonymous import AnonymousListView, AnonymousDetailView
from main.views.post import PostListView, PostDetailView
from main.views.comment import CommentListView, CommentDetailView

# 카페 및 장소 관련 뷰
from main.views.cafe import NearbyCafeListView, NearbyCafeDetailView
from main.views.rating import RatingListView, RatingDetailView
from main.views.review import ReviewListView, ReviewDetailView

#길찾기 관련 뷰
from main.views.direction import find_meeting_cafe, find_single_user_direction

schema_view = get_schema_view(
    openapi.Info(
        title="Nomad_Kor API Documentation",
        default_version='v1',
        description="API 문서입니다. JWT 토큰을 사용하여 인증이 가능합니다.",
        contact=openapi.Contact(email="chsm7288@naver.com"),
        license=openapi.License(name="Custom License"),
    ),
    public=True,
    permission_classes=([permissions.AllowAny]),
    authentication_classes=[],  # 인증 클래스를 추가합니다
)

urlpatterns = [
    # 관리자 페이지
    path('admin/', admin.site.urls),

    # JWT 토큰
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger URLs 추가
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # 인증 및 프로필
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/create/', create_profile, name='create_profile'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),

    # 카페 관련
    path('cafes/nearby/', NearbyCafeListView.as_view(), name='nearby-cafes'),  # 주변 카페 목록 조회
    path('cafes/nearby/<int:cafe_id>/', NearbyCafeDetailView.as_view(), name='nearby-cafe-detail'),  # 카페 상세 조회

    path('cafes/<int:cafe_id>/ratings/', RatingListView.as_view(), name='rating-list'),  # 특정 카페의 별점 목록 조회 및 추가
    path('cafes/<int:cafe_id>/ratings/<int:pk>/', RatingDetailView.as_view(), name='rating-detail'),
    # 특정 카페의 개별 별점 수정 및 삭제
    path('cafes/<int:cafe_id>/reviews/', ReviewListView.as_view(), name='review-list'),  # 특정 카페의 리뷰 목록 조회 및 작성
    path('cafes/<int:cafe_id>/reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    # 특정 카페의 개별 리뷰 수정 및 삭제

    # 길찾기
    path('directions/meeting/', find_meeting_cafe, name='find-meeting-cafe'),
    path('directions/single/', find_single_user_direction, name='find-single-user-direction'),

    # Position 게시판
    path('network/position/', PositionListView.as_view(), name='position-list'),
    path('network/position/<int:pk>/', PositionDetailView.as_view(), name='position-detail'),
    # Position 게시판의 게시글
    path('network/position/<int:position_id>/posts/', PostListView.as_view(), name='position-post-list'),
    path('network/position/<int:position_id>/posts/<int:pk>/', PostDetailView.as_view(), name='position-post-detail'),
    # Position 게시판 댓글
    # 게시글에 대한 댓글을 작성하기 위한 URL
    path('network/position/<int:position_id>/posts/<int:post_id>/comments/', CommentListView.as_view(),
         name='position-comment-list'),
    path('network/position/<int:position_id>/posts/<int:post_id>/comments/<int:pk>/', CommentDetailView.as_view(),
         name='position-comment-detail'),

    # FTF 게시판
    path('network/ftf/', FTFListView.as_view(), name='ftf-list'),
    path('network/ftf/<int:id>/', FTFDetailView.as_view(), name='ftf-detail'),  # <int:id>로 수정
    path('network/ftf/<int:ftf_id>/posts/', PostListView.as_view(), name='ftf-post-list'),
    path('network/ftf/<int:ftf_id>/posts/<int:pk>/', PostDetailView.as_view(), name='ftf-post-detail'),
    path('network/ftf/<int:ftf_id>/posts/<int:post_id>/comments/', CommentListView.as_view(), name='ftf-comment-list'),
    path('network/ftf/<int:ftf_id>/posts/<int:post_id>/comments/<int:pk>/', CommentDetailView.as_view(), name='ftf-comment-detail'),

    # 익명 게시판
    path('network/anonymous/', AnonymousListView.as_view(), name='anonymous-list'),
    path('network/anonymous/<int:pk>/', AnonymousDetailView.as_view(), name='anonymous-detail'),
    path('network/anonymous/<int:anonymous_id>/posts/', PostListView.as_view(), name='anonymous-post-list'),
    path('network/anonymous/<int:anonymous_id>/posts/<int:pk>/', PostDetailView.as_view(), name='anonymous-post-detail'),
    path('network/anonymous/<int:anonymous_id>/posts/<int:post_id>/comments/', CommentListView.as_view(), name='anonymous-comment-list'),
    path('network/anonymous/<int:anonymous_id>/posts/<int:post_id>/comments/<int:pk>/', CommentDetailView.as_view(), name='anonymous-comment-detail'),
]

# 미디어 파일 제공 (개발 환경에서만)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
