from rest_framework import serializers
from ..models.cafe import Cafe
from datetime import datetime
from django.utils.timezone import now, localtime


class CafeSerializer(serializers.ModelSerializer):
    is_open = serializers.SerializerMethodField()  # 동적으로 계산되는 필드
    opening_hours = serializers.SerializerMethodField()  # 포맷팅된 영업 시간 필드
    distance = serializers.FloatField(source='calculated_distance')
    class Meta:
        model = Cafe
        fields = [
            'name',           # 장소 이름 (지점 + 이름 통합)
            'address',        # 주소
            'opening_hours',  # 친절하게 포맷팅된 영업 시간
            'latitude',
            'longitude',
            'is_open',        # 영업 상태 ("영업 전", "영업 중", "영업 종료")
            'distance'
        ]

    def get_opening_hours(self, obj):
        """
        영업 시간 필드를 "HH:MM까지" 형식으로 반환.
        """
        if obj.opening_hours:
            try:
                start_time, end_time = obj.opening_hours.split("-")
                start_time = start_time.strip()
                end_time = end_time.strip()
                return f"{start_time} - {end_time}"  # 친절하게 포맷팅된 영업 시간 반환
            except ValueError:
                return "영업 시간 정보가 잘못되었습니다."
        return None  # 영업 시간 정보가 없는 경우

    def get_is_open(self, obj):
        """
        현재 영업 상태를 반환.
        """
        if obj.opening_hours:
            try:
                # "08:00 - 20:00" 형식에서 시작 및 종료 시간 추출
                start_time, end_time = obj.opening_hours.split("-")
                start_time = datetime.strptime(start_time.strip(), "%H:%M").time()  # 시간 변환
                end_time = datetime.strptime(end_time.strip(), "%H:%M").time()

                # 현재 시간을 로컬 시간으로 변환
                current_time = localtime(now()).time()
                print(f"DEBUG: Start={start_time}, End={end_time}, Current={current_time}")  # 디버깅 로그

                # 영업 상태 판단
                if start_time <= current_time <= end_time:
                    return "영업 중"
                elif current_time < start_time:
                    return "영업 전"
                else:
                    return "영업 종료"
            except ValueError:
                # 형식이 잘못된 경우 처리
                return "영업 시간 정보가 잘못되었습니다."
        return "영업 시간 정보가 제공되지 않았습니다."
