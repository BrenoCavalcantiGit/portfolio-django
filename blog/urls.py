from django.urls import path

from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('home/', views.home, name='home'),
]
