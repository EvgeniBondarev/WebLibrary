from django.urls import path
from . import views


urlpatterns = [
    path('', views.login),
    path('registration', views.registration),
    path('user_page', views.user_page),
    path('user_books', views.user_books),
    path('all_books', views.all_books),
    path('book_loans', views.book_loan_list_view)
]