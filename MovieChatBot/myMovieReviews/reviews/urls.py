from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("", views.main_movie_list, name="main"),
    path("reviews/", views.reviews_list, name="list"),
    path("reviews/create/", views.review_create, name="create"),
    path("reviews/<int:pk>/update/", views.review_update, name="update"),
    path("reviews/<int:pk>/delete/", views.review_delete, name="delete"),
    path("movies/<int:pk>/", views.movie_detail, name="movie_detail"),
    path("chat/", views.chatbot, name="chatbot"),
]
