from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/', views.get_redirect_url, name='redirect'),
    path('details/', views.detail, name='detail'),
    path('show/', views.show, name='show'),
]
