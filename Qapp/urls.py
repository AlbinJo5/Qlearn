from django.contrib import admin
from . import views
from django.urls import path, include


urlpatterns = [
    path('index/<str:user>', views.index, name="index"),
    path('<str:user>/<str:dfName>/<int:setNum>', views.work, name="work"),
    path('signup/', views.signup, name="signup"),
    path('', views.signin, name="signin"),
    path('work2/', views.work2, name="work2"),

]