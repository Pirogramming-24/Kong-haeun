from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('edit/', views.profile_edit, name='profile_edit'),
    path('search/', views.user_search, name='search'),
    path('follow/<int:user_id>/', views.follow_toggle, name='follow_toggle'),
    path('<str:username>/', views.profile, name='profile'),
]
