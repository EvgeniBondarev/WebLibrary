from django.urls import path
from . import views


urlpatterns = [
    path('', views.login),
    path('registration', views.registration),
    path('user_page', views.user_page)
]