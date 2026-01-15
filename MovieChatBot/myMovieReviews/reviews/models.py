from django.db import models

# Create your models here.
class Review(models.Model):
    title = models.CharField(max_length=32) # 제목
    release_year = models.PositiveIntegerField() # 개봉년도
    genre = models.CharField(max_length=32) # 장르
    score = models.FloatField() # 별점
    director = models.CharField(max_length=32) # 감독
    actor = models.CharField(max_length=32) # 주연
    running_time = models.PositiveIntegerField() # 러닝타임
    content = models.TextField()  # 리뷰내용

    def __str__(self):
        return self.title
    
class Movie(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True) # TMDB 고유 ID
    title = models.CharField(max_length=200) # 영화 제목
    overview = models.TextField(blank=True) # 줄거리
    poster_path = models.CharField(max_length=255, blank=True) # 포스터 경로
    release_year = models.PositiveIntegerField(null=True, blank=True) # 개봉년도
    director = models.CharField(max_length=200, blank=True) # 감독
    actors = models.TextField(blank=True) # 배우
 
    def __str__(self):
        return self.title