from django.db import models

# Create your models here.
class Movie(models.Model):
    tmdb_id = models.PositiveIntegerField(unique=True, null=True, blank=True) # TMDB 고유 ID
    title = models.CharField(max_length=200) # 영화 제목
    overview = models.TextField(blank=True) # 줄거리
    poster_image = models.ImageField( # 포스터 이미지
        upload_to="posters/",
        blank=True,
        null=True
    )
    poster_path = models.CharField(max_length=255, blank=True) # 포스터 경로 (TMDB용)
    director = models.CharField(max_length=200, blank=True) # 감독
    actors = models.TextField(blank=True) # 배우
    genre = models.CharField(max_length=32, blank=True) # 장르
    release_year = models.PositiveIntegerField(null=True, blank=True) # 개봉년도
    running_time = models.PositiveIntegerField(null=True, blank=True) # 러닝타임

    is_from_tmdb = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Review(models.Model):
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    
    score = models.FloatField() # 별점
    content = models.TextField()  # 리뷰내용
    created_at = models.DateTimeField(auto_now_add=True) # 생성일