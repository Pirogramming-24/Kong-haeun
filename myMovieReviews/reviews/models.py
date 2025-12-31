from django.db import models

# Create your models here.
# Django에서 모델 하나 = DB 테이블 하나
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
    
# modles.py 수정 -> migration으로 데이터베이스 반영
# python manage.py makemigrations - 모델 변경 사항을 바탕으로 migration 파일 생성
# python manage.py showmigrations - 어떤 migration이 있고, 적용되었는지 확인(optional)
# python manage.py migrate - migration을 실행해서 실제로 DB에 테이블 생성