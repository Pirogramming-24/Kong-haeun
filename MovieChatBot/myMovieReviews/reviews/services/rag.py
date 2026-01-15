from django.db.models import Q
from reviews.models import Movie, Review

def search_context(question, limit=5):
    movies = Movie.objects.filter(
        Q(title__icontains=question) |
        Q(overview__icontains=question) |
        Q(director__icontains=question) |
        Q(actors__icontains=question)
    )[:limit]

    reviews = Review.objects.filter(
        Q(title__icontains=question) |
        Q(content__icontains=question)
    )[:limit]

    context = []

    for m in movies:
        context.append(
            f"영화 제목: {m.title}\n줄거리: {m.overview}"
        )

    for r in reviews:
        context.append(
            f"리뷰 제목: {r.title}\n리뷰 내용: {r.content}"
        )

    return "\n\n".join(context)
