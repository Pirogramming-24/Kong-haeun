from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
	path('', views.reviews_list, name='list'), # path(URL, 실행함수, 이름)
    path('<int:pk>/', views.review_detail, name='detail'),
    path('create/', views.review_create, name='create'),
    path('<int:pk>/update/',views.review_update,name='update'),
    path('<int:pk>/delete/',views.review_delete,name='delete'),
    path('movies/',views.movie_list,name='movie_list'),
    path('movies/<int:pk>/',views.movie_detail,name='movie_detail'),
]