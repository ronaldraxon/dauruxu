from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register_page, name="register"),
    path('login/', views.login_page, name="login"),
    #path('classification_models/', views.classification_models),
    #path('users/', views.users),
]