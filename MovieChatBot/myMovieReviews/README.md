## 필요한 패키지

필요한 패키지
`pip install django pillow python-dotenv requests openai`

각 패키지의 역할
- `django`: 웹 프레임워크
- `pillow`: 이미지 처리 (포스터 업로드)
- `python-dotenv`: 환경 변수 관리
- `requests`: HTTP 요청 (TMDB API 호출)
- `openai`: OpenAI API 사용


## TMDB 데이터 불러오기 방법

1. TMDB API KEY 발급

2. 프로젝트 루트에 `.env` 파일 생성
TMDB_API_KEY=발급받은_키

3. 쉘 실행
python manage.py shell

4. 영화 데이터 import (기본 설정 기준 TMDB 인기 영화 최대 40개(2페이지)를 가져옵니다.)
from reviews.services.movie_importer import import_popular_movies
import_popular_movies()


## 영화 추천 챗봇

1. UPSTAGE API KEY 발급

2. 프로젝트 루트에 `.env` 파일 생성
UPSTAGE_API_KEY=발급받은_키