from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('video/<int:pk>/', views.video_detail, name='video_detail'),
    path('youtube/<str:video_id>/', views.youtube_video_detail, name='youtube_video_detail'),
    path('upload/', views.upload_video, name='upload'),
    path('like/<int:pk>/', views.toggle_like, name='toggle_like'),
    path('subscribe/<int:user_id>/', views.toggle_subscribe, name='toggle_subscribe'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('channel/<int:user_id>/', views.channel_view, name='channel'),
]
