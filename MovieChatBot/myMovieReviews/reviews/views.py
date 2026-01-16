from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Review, Movie
from reviews.services.rag import search_context
from reviews.services.llm import ask_llm
from django.core.paginator import Paginator

# Create your views here.
# 메인페이지(첫 화면)
def main_movie_list(request):
    query = request.GET.get("q", "") # 검색
    filter_type = request.GET.get("filter", "all") # 필터
    sort = request.GET.get("sort", "latest") # 정렬

    movies = Movie.objects.all()

    # 검색
    if query:
        movies = movies.filter(
            Q(title__icontains=query) | # 대소문자 무시, 부분일치 검색
            Q(director__icontains=query) |
            Q(actors__icontains=query)
        )

    # 필터
    if filter_type == "tmdb":
        movies = movies.filter(is_from_tmdb=True)
    elif filter_type == "custom":
        movies = movies.filter(is_from_tmdb=False)

    # 정렬
    if sort == "title":
        movies = movies.order_by("title")
    elif sort == "year":
        movies = movies.order_by("-release_year")
    else:
        movies = movies.order_by("-id")

    # 페이지네이션
    paginator = Paginator(movies, 12)
    page_number = request.GET.get("page")
    movies = paginator.get_page(page_number)

    total_count = Movie.objects.count()
    tmdb_count = Movie.objects.filter(is_from_tmdb=True).count()
    custom_count = Movie.objects.filter(is_from_tmdb=False).count()

    context = {
        "movies":movies,
        "query":query,
        "filter": filter_type,
        "sort":sort,
        "total_count": total_count,
        "tmdb_count": tmdb_count,
        "custom_count": custom_count,
    }
    return render(request, "main_movie_list.html",context)

# 영화 상세, 리뷰 목록
def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = movie.reviews.all()

    # 리뷰 추가 처리
    if request.method == "POST":
        Review.objects.create(
            movie=movie,
            score=request.POST["score"],
            content=request.POST["content"],
        )
        return redirect("reviews:movie_detail", pk=pk)

    return render(request, "movie_detail.html", {
        "movie": movie,
        "reviews": reviews,
    })


# 리뷰 작성 (직접 추가 영화)
def review_create(request):
    if request.method == "POST":
        movie, _ = Movie.objects.get_or_create(
            title=request.POST["title"],
            is_from_tmdb=False,
            defaults={
                "release_year": request.POST.get("release_year"),
                "director": request.POST.get("director"),
                "actors": request.POST.get("actor"),
                "genre": request.POST.get("genre"),
                "running_time": request.POST.get("running_time"),
                "poster_image": request.FILES.get("poster_image"),
            }
        )

        Review.objects.create(
            movie=movie,
            score=request.POST["score"],
            content=request.POST["content"],
        )

        return redirect("reviews:main")

    return render(request, "review_create.html")

# 리뷰 수정
def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if request.method == "POST":
        review.score = request.POST["score"]
        review.content = request.POST["content"]
        review.save()
        return redirect("reviews:movie_detail", pk=review.movie.id)

    return render(request, "review_update.html", {"review": review})

# 리뷰 삭제
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    movie_id = review.movie.id

    if request.method == "POST":
        review.delete()

    return redirect("reviews:movie_detail", pk=movie_id)

# 전체 리뷰
def reviews_list(request):
    reviews = Review.objects.select_related("movie")

    sort = request.GET.get("sort", "latest")

    if sort == "score":
        reviews = reviews.order_by("-score")
    elif sort == "title":
        reviews = reviews.order_by("movie__title")
    else:
        reviews = reviews.order_by("-created_at")

    return render(request, "reviews_list.html", {
        "reviews": reviews,
        "sort": sort,
    })

# 챗봇
def chatbot(request):
    # 초기화
    if request.GET.get("reset"):
        request.session.pop("chat_history", None)
        return redirect("reviews:chatbot")
        
    history = request.session.get("chat_history", [])

    if request.method == "POST":
        question = request.POST.get("question")

        if question:
            # R: DB 검색
            context = search_context(question)

            # A + G: LLM 호출
            answer = ask_llm(question, context)

            # 대화 기록에 추가
            history.append({
                "question": question,
                "answer": answer,
            })

            # 세션에 다시 저장
            request.session["chat_history"] = history

    return render(request, "chatbot.html", {
        "history": history,
    })