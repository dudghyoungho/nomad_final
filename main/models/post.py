# models/post.py
from django.db import models


class Post(models.Model):
    # 각 게시판에 대해 다른 ForeignKey 필드
    position = models.ForeignKey('Position', on_delete=models.CASCADE, null=True, blank=True)  # Position 게시판
    ftf = models.ForeignKey('FTF', on_delete=models.CASCADE, null=True, blank=True)  # FTF 게시판
    anonymous = models.ForeignKey('Anonymous', on_delete=models.CASCADE, null=True, blank=True)  # 익명 게시판

    author = models.ForeignKey('Profile', on_delete=models.CASCADE)  # 작성자
    author_name = models.CharField(max_length=100)  # 작성자 이름 (익명 게시판은 "익명", 일반 게시판은 닉네임)
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
