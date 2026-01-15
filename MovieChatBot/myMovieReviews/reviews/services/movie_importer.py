# TMDB에서 가져온 영화들을 Movie 모델(DB)에 실제로 넣어주는 실행 담당자
from reviews.models import Movie
from reviews.services.tmdb import get_popular_movies

def import_popular_movies():
    movies = get_popular_movies()
    created_count = 0
    
    for m in movies:
        release_year = None
        if m.get("release_date"):
            release_year = int(m["release_date"][:4])
        
        _,created = Movie.objects.get_or_create(
            tmdb_id=m["id"],
            defaults={
                "title":m["title"],
                "overview":m.get("overview",""),
                "poster_path":m.get("poster_path",""),
                "release_year":release_year,
            }
        )

        if created:
            created_count += 1
    
    return created_count # 이번 실행에서 새로 추가된 영화 수