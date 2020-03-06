from django.urls import path
from django.conf.urls import include
from . import views


    
urlpatterns = [
    path('', views.index, name='index'),
	path('login/', views.login_view, name='login'),
	path('register/', views.register_view, name = "register"),
]
