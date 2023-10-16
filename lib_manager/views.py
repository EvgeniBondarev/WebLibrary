from django.shortcuts import render, redirect

from .forms import LogIn, Register
from .models import Reader, BookLoan


def login(request):
    """Логин пользователя"""
    if request.method == "POST":
        login_form = LogIn(request.POST)
        if login_form.is_valid():
            reader = login_form.cleaned_data['readers']
            return redirect(f"/user_page?reader_id={reader.pk}")
        else:
            login_form = LogIn()
            return render(request, "login.html", {"form": login_form})
    else:
        login_form = LogIn()
        return render(request, "login.html", {"form": login_form})


def registration(request):
    if request.method == "POST":
        reader = Register(request.POST)
        if reader.is_valid():
            reader.save()
            login_form = LogIn()
            return render(request, "login.html", {"form": login_form})
        else:
            registr_form = Register()
            return render(request, "registration.html", {"form": registr_form})
    else:
        registr_form = Register()
        return render(request, "registration.html", {"form": registr_form})


def user_page(request):
    """Главная страница пользователя"""
    reader_id = request.GET.get("reader_id")

    if reader_id:
        user = Reader.objects.get(pk=reader_id)
        book_loans = BookLoan.objects.filter(reader_id=reader_id)

        return render(request, "base.html", {"user": user, 'book_loans': book_loans})
    else:
        login_form = LogIn()
        return render(request, "login.html", {"form": login_form})



