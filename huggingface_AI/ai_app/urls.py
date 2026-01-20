from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name="home"),

    path("summarize/",views.summarize,name="summarize"), # 요약
    path("sentiment/",views.sentiment,name="sentiment"), # 감정분석
    path("generate/",views.generate,name="generate"),    # 텍스트 생성
]