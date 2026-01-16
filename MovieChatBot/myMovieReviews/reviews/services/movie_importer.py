# TMDB에서 가져온 영화 데이터를 Movie 모델(DB)에 저장하는 실행 모듈

from reviews.models import Movie
from reviews.services.tmdb import (
    get_popular_movies,
    get_movie_detail,
    get_movie_credits,
)

def import_popular_movies():
    created_count = 0

    for page in [1, 2]:
        movies = get_popular_movies(page=page)
    
        for m in movies:
            tmdb_id = m["id"]

            # 이미 있으면 skip
            if Movie.objects.filter(tmdb_id=tmdb_id).exists():
                continue

            detail = get_movie_detail(tmdb_id)
            credits = get_movie_credits(tmdb_id)
            
            # 감독 추출
            director = ""
            for crew in credits.get("crew", []):
                if crew["job"] == "Director":
                    director = crew["name"]
                    break

            # 배우 5명만 추출
            actors = [
                cast["name"]
                for cast in credits.get("cast",[])[:5]
            ]

            # 개봉 연도
            release_year = None
            if m.get("release_date"):
                release_year = int(m["release_date"][:4])

            movie, created = Movie.objects.update_or_create(
                tmdb_id=m["id"],
                defaults={
                    "title": m["title"],
                    "release_year": release_year,
                    "overview": m.get("overview", ""),
                    "poster_path": m.get("poster_path", ""),
                    "director": director,
                    "actors": ", ".join(actors),
                    "is_from_tmdb": True,
                }
            )

            if created:
                created_count += 1
    
    return created_count # 이번 실행에서 새로 추가된 영화 수