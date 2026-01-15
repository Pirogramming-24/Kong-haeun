from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from .models import Review, Movie
from reviews.services.rag import search_context

# Create your views here.
def reviews_list(request): # DB 여러 개
    reviews = Review.objects.all() # DB에 저장된 모든 리뷰 조회

    # 정렬 기능
    sort = request.GET.get('sort')
    if sort == 'title':
        reviews = Review.objects.order_by('title') # A->Z
    elif sort == 'score':
        reviews = Review.objects.order_by('-score') # 별점 높은 순
    elif sort == 'running_time':
        reviews = Review.objects.order_by('running_time') # 러닝타임 짧은 순
    else:
        reviews = Review.objects.all() # 기본 정렬

    context = {"reviews":reviews}
    return render(request,"reviews_list.html",context) # HTML 템플릿에 데이터 넘김

def review_detail(request,pk): # DB 1개 (pk 필요)
    review = Review.objects.get(id=pk) #DB에서 id가 pk인 게시글 하나 조회

    hours = review.running_time // 60 # 분-> 시간
    minutes = review.running_time % 60
    running_time_display = f"{hours}시간 {minutes}분"

    context = {"review":review, "running_time_display":running_time_display}
    return render(request,"review_detail.html",context)

def review_create(request): # 제목, 개봉년도, 감독, 주연, 장르, 별점, 러닝타임, 리뷰내용
    # POST인 경우 (작성 완료 버튼 클릭) - 저장
    if request.method == "POST":
        Review.objects.create(
             # 'models.py에 정의된 필드명'에 'HTML 폼에서 사용자가 입력한 값'을 넣겠다
            title=request.POST['title'],
            release_year=request.POST['release_year'],
            director=request.POST['director'],
            actor=request.POST['actor'],
            genre=request.POST['genre'],
            score=request.POST['score'],
            running_time=request.POST['running_time'],
            content=request.POST['content'],
        )
        return redirect("reviews:list") # 리뷰 저장 후 리뷰 목록 페이지로 이동
    # POST 요청은 서버 상태를 변경: 중복 요청 방지 위해 redirect 사용
    
    # GET인 경우 (페이지 처음 들어올 때) - 폼
    return render(request,'review_create.html') # 리뷰 작성 화면을 렌더링
    # GET 요청은 화면만 보여줌: 화면 출력을 위해 render 사용

def review_update(request,pk):
    # POST인 경우 (수정 완료 버튼 클릭) - 덮어쓰기
    review = Review.objects.get(id=pk) # URL에서 받은 pk로 DB에서 리뷰 조회
    if request.method == "POST":
        review.title=request.POST['title']
        review.release_year=request.POST['release_year']
        review.director=request.POST['director']
        review.actor=request.POST['actor']
        review.genre=request.POST['genre']
        review.score=request.POST['score']
        review.running_time=request.POST['running_time']
        review.content=request.POST['content']
        review.save()
        return redirect("reviews:detail",pk=pk) # 수정한 해당 리뷰 디테일 페이지로 이동
    
    # GET인 경우 (페이지 처음 들어올 때) - 기존 값
    context = {"review":review} # 값 채워진 상태로
    return render(request,'review_update.html',context) # 리뷰 수정 화면을 렌더링

def review_delete(request,pk):
    # POST 요청일 때만 삭제 → 실수로 URL을 눌러 삭제되는 것을 방지
    # GET 요청은 아무 일도 안 함
    if request.method == "POST":
        review = Review.objects.get(id=pk) # pk로 삭제 대상 리뷰를 DB에서 조회
        review.delete() # 해당 리뷰를 DB에서 완전히 삭제
    return redirect('reviews:list') # 삭제 후 리뷰 목록 페이지로 리다이렉트


# Movie용 view
def movie_list(request):
    query = request.GET.get("q","") # 검색어
    sort = request.GET.get("sort","") # 정렬
    
    movies = Movie.objects.all()

    # 검색
    if query:
        movies = Movie.objects.filter(
            Q(title__icontains=query) | # 대소문자 무시, 부분일치 검색
            Q(director__icontains=query) |
            Q(actors__icontains=query)
        )
    
    # 정렬
    if sort == "title":
        movies = movies.order_by("title")
    elif sort == "latest":
        movies = movies.order_by("-release_year")

    # 40개 제한
    movies = movies[:40]

    context = {
        "movies":movies,
        "query":query,
        "sort":sort,
    }
    return render(request, "movie_list.html",context)

def movie_detail(request, pk):
    movie = get_object_or_404(Movie, id=pk)

    return render(request, "movie_detail.html", {
        "movie": movie,
    })

def chatbot(request):
    return render(request, "chatbot.html")