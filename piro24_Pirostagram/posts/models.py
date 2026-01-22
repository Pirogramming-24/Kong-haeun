from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model): # 작성자, 이미지, 내용, 작성 시간
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    image = models.ImageField(upload_to='posts/')
    content = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
