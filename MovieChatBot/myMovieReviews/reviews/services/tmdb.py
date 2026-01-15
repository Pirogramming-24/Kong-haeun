# TMDB(외부 영화 서버)와 통신하는 전담 담당자

import os
import requests

TMDB_BASE_URL = "https://api.themoviedb.org/3"

# TMDB API 키 가져오기 -> 결과(JSON)를 Python 데이터로 돌려주기
def get_popular_movies(page=1):
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        raise RuntimeError("TMDB_API_KEY가 설정되지 않았습니다.")

    url = f"{TMDB_BASE_URL}/movie/popular"
    params = {
        "api_key":api_key,
        "language":"ko-KR",
        "page":page,
    }

    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    return res.json()["results"]

# TMDB 영화 1개에 대한 상세 JSON 반환
def get_movie_detail(tmdb_id):
    api_key = os.getenv("TMDB_API_KEY")
    if not api_key:
        raise RuntimeError("TMDB_API_KEY가 설정되지 않았습니다.")

    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}"
    params = {
        "api_key":api_key,
        "language":"ko-KR",
    }

    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    return res.json()