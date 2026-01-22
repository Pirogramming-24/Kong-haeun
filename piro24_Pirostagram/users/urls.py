from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('follow/<int:user_id>/', views.follow_toggle, name='follow_toggle'),
    path('edit/', views.profile_edit, name='profile_edit'),
    path('<str:username>/', views.profile, name='profile'),
]
