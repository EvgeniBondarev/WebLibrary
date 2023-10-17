from django.shortcuts import render, redirect, HttpResponse

from .forms import LogIn, Register, BookCode
from .models import Reader, BookLoan, Book
from datetime import datetime


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

def user_books(request):
    """Список книг пользователя с возможностью их возврата"""
    reader_id = request.GET.get("reader_id")
    if request.method == "POST":
        book_code = BookCode(request.POST)
        if book_code.is_valid():
            try:
                code = book_code.cleaned_data['code']

                book = Book.objects.get(code=int(code))
                reader = Reader.objects.get(pk=reader_id)
                book_loan = BookLoan.objects.get(book=book, return_date=None, reader=reader)

                book_loan.return_date = datetime.now()
                book_loan.save()

                book.is_visible = True
                book.save()

                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

            except Book.DoesNotExist:
                return HttpResponse("Книга не найдена")

            except BookLoan.DoesNotExist:
                return HttpResponse(f"Соответствующая запись для '{ reader.first_name } { reader.middle_name }' не найдена")
        else:
            user = Reader.objects.get(pk=reader_id)
            user_books = BookLoan.objects.filter(reader_id=reader_id, return_date__isnull=True)
            book_form = BookCode()
            return render(request, "user_books.html", {'user': user, 'user_books': user_books, 'form': book_form})
    else:
        user = Reader.objects.get(pk=reader_id)
        user_books = BookLoan.objects.filter(reader_id=reader_id, return_date__isnull=True)
        book_form = BookCode()
        return render(request, "user_books.html", {'user': user, 'user_books': user_books, 'form': book_form})

def all_books(request):
    """Вывод списка всех книг с возможностью их выдачи"""
    reader_id = request.GET.get("reader_id")
    user = Reader.objects.get(pk=reader_id)
    books = Book.objects.filter(is_visible=True)

    book_code = BookCode(request.POST)
    if request.method == "POST":
        if book_code.is_valid():
            try:
                code = book_code.cleaned_data['code']
                book = Book.objects.get(code=int(code))
                reader = Reader.objects.get(pk=reader_id)

                book_loan = BookLoan(book=book, reader=reader)
                book_loan.save()

                book.is_visible = False
                book.save()

                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

            except Book.DoesNotExist:
                return HttpResponse("Книга не найдена")

            except BookLoan.DoesNotExist:
                return HttpResponse(f"Соответствующая запись для '{ reader.first_name } { reader.middle_name }' не найдена")
        else:
            registr_form = Register()
            return render(request, "registration.html", {"form": registr_form})
    else:
        book_form = BookCode()
        return render(request, "all_books.html", {'user': user, 'books': books, 'form': book_form})

def book_loan_list_view(request):
    book_loans = BookLoan.objects.all()
    return render(request, 'book_loans.html', {'book_loans': book_loans})

