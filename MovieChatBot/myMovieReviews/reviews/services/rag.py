from django.db.models import Q
from reviews.models import Review

def search_context(query):
    reviews = Review.objects.select_related("movie").filter(
        Q(content__icontains=query) |
        Q(movie__title__icontains=query) |
        Q(movie__director__icontains=query) |
        Q(movie__actors__icontains=query)
    )

    texts = []
    for r in reviews:
        texts.append(
            f"""
            영화 제목: {r.movie.title}
            감독: {r.movie.director}
            배우: {r.movie.actors}
            리뷰 내용: {r.content}
            평점: {r.score}
            """
        )

    return "\n".join(texts)
