# TMDB(외부 영화 API 서버)와 통신하는 서비스 모듈
# TMDB API 호출 로직을 View/Model과 분리하여 관리
# TMDB로부터 받은 JSON 응답을 Python dict 형태로 반환

import os
import requests

TMDB_BASE_URL = "https://api.themoviedb.org/3"

# TMDB 인기 영화 목록 조회
# page 번호에 해당하는 인기 영화 리스트(JSON)를 반환
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

# TMDB 영화 단일 상세 정보 조회
# 영화 ID(tmdb_id)를 기준으로 상세 정보(JSON)를 반환
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

# TMDB 영화 크레딧(감독/배우) 정보 조회
# 영화 ID(tmdb_id)를 기준으로 감독, 배우 정보(JSON)를 반환
def get_movie_credits(tmdb_id):
    api_key = os.getenv("TMDB_API_KEY")
    
    url = f"{TMDB_BASE_URL}/movie/{tmdb_id}/credits"
    params = {
        "api_key":api_key,
        "language":"ko-KR",
    }

    res = requests.get(url, params=params, timeout=10)
    res.raise_for_status()
    return res.json()