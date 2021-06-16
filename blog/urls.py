from django.urls import path

from . import views

app_name='blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<str:pk>/', views.PostView.as_view(), name='post'),
]
