from django.db import models
from django.conf import settings
from .cafe import Cafe

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,blank=True)  # 별점 작성자
    cafe = models.ForeignKey(Cafe, related_name='ratings', on_delete=models.CASCADE)  # 대상 장소
    rating = models.PositiveSmallIntegerField()  # 별점 (1~5)
    created_at = models.DateTimeField(auto_now_add=True)  # 작성 시간

    class Meta:
        unique_together = ('user', 'cafe')  # 유저가 같은 장소에 중복 별점 주는 것을 방지

    def __str__(self):
        return f"{self.user.username} - {self.cafe.name} ({self.rating} stars)"
