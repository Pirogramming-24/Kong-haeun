from django.urls import path
from . import views

app_name='posts'

urlpatterns = [
    path('', views.feed, name='feed'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),

    path('<int:pk>/comments/create/', views.comment_create, name='comment_create'),
    path('<int:pk>/comments/<int:comment_pk>/update/', views.comment_update, name='comment_update'),
    path('<int:pk>/comments/<int:comment_pk>/delete/', views.comment_delete, name='comment_delete'),

]