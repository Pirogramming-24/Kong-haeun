from django.urls import path
from . import views

app_name = 'reviews'

# MODEL -> URL -> VIEW -> TEMPLATE 로 작성
# 브라우저 요청 → urls.py → views.py → (models.py) → template → 응답

urlpatterns = [
	path('', views.reviews_list, name='list'), # path(URL, 실행함수, 이름)
    path('<int:pk>/', views.review_detail, name='detail'),
    path('create/', views.review_create, name='create'),
    path('<int:pk>/update/',views.review_update,name='update'),
    path('<int:pk>/delete/',views.review_delete,name='delete'),
]