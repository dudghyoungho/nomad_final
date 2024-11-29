from django.db import models
from datetime import datetime
from django.utils.timezone import now


class Cafe(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300, blank=True, null=True)
    isConcentrate = models.BooleanField(default=False)  # 집중하기 좋은 카페
    opening_hours = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    distance = models.FloatField(null=True, blank=True)

    def get_status(self):
        """
        현재 시간에 따라 영업 상태 반환:
        - "영업 전"
        - "영업 중"
        - "영업 종료"
        - "영업 시간 정보를 제공해주지 않는 카페입니다."
        """
        if not self.opening_hours:
            return "영업 시간 정보를 제공해주지 않는 카페입니다."

        try:
            start_time, end_time = self.opening_hours.split("-")
            current_time = now().time()
            start_time = datetime.strptime(start_time.strip(), "%H:%M").time()
            end_time = datetime.strptime(end_time.strip(), "%H:%M").time()

            if current_time < start_time:
                return "영업 전"
            elif start_time <= current_time <= end_time:
                return "영업 중"
            else:
                return "영업 종료"
        except ValueError:
            return "영업 시간 정보를 제공해주지 않는 카페입니다."  # 잘못된 형식의 영업 시간도 처리

    def __str__(self):
        return self.name



