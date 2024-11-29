from django.db import models
from .cafe import Cafe
from .profile import Profile

class Review(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE, related_name='reviews')  # 리뷰가 속한 장소
    user = models.ForeignKey(Profile, on_delete=models.CASCADE,null=True, blank=True)  # 리뷰 작성자
    content = models.TextField()  # 리뷰 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 리뷰 작성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 리뷰 수정 시간

    def __str__(self):
        return f"Review by {self.user} for {self.cafe}"

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
