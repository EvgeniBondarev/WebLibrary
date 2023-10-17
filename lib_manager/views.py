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
            return render(request, "login.html", {"form": login_form, 'error_message': 'Данные формы не валидны'})

    login_form = LogIn()
    return render(request, "login.html", {"form": login_form})


def registration(request):
    if request.method == "POST":
        registration_form = Register(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            return redirect('/')
        else:
            return render(request, "registration.html", {"form": registration_form, 'error_message': 'Данные формы не валидны'})

    registration_form = Register()
    return render(request, "registration.html", {"form": registration_form})


def user_page(request):
    """Главная страница пользователя"""
    reader_id = request.GET.get("reader_id")

    if reader_id:
        try:
            user = Reader.objects.get(pk=reader_id)
            book_loans = BookLoan.objects.filter(reader_id=reader_id)
            return render(request, "base.html", {"user": user, 'book_loans': book_loans})
        except Reader.DoesNotExist:
            pass
    login_form = LogIn()
    return render(request, "login.html", {"form": login_form})

def user_books(request):
    """Список книг пользователя с возможностью их возврата"""
    reader_id = request.GET.get("reader_id")
    user = Reader.objects.get(pk=reader_id)
    user_books = BookLoan.objects.filter(reader_id=reader_id, return_date__isnull=True)

    if request.method == "POST":
        book_form = BookCode(request.POST)

        if book_form.is_valid():
            code = book_form.cleaned_data['code']
            try:
                book = Book.objects.get(code=int(code))
                book_loan = BookLoan.objects.get(book=book, return_date=None, reader=user)
                book_loan.return_date = datetime.now()
                book_loan.save()
                book.is_visible = True
                book.save()
                return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

            except Book.DoesNotExist:
               return render(request, "user_books.html", {'user': user, 'user_books': user_books, 'form': book_form, 'error_message': 'Книга не найдена'})

            except BookLoan.DoesNotExist:
                return render(request, "user_books.html", {'user': user, 'user_books': user_books, 'form': book_form, 'error_message': f"Соответствующая запись для "
                                                                                                                                      f"'{user.first_name} {user.middle_name}'"
                                                                                                                                       f" не найдена"})
        else:
            return render(request, "user_books.html", {'user': user, 'user_books': user_books, 'form': book_form, 'error_message': 'Данные формы не валидны'})
    else:
        book_form = BookCode()
        return render(request, "user_books.html", {'user': user, 'user_books': user_books, 'form': book_form})

def all_books(request):
    """Вывод списка всех книг с возможностью их выдачи"""
    reader_id = request.GET.get("reader_id")
    user = Reader.objects.get(pk=reader_id)
    books = Book.objects.filter(is_visible=True)

    if request.method == "POST":
        book_form = BookCode(request.POST)
        if book_form.is_valid():
            code = book_form.cleaned_data['code']
            try:
                book = Book.objects.get(code=int(code))
                reader = Reader.objects.get(pk=reader_id)

                if BookLoan.objects.filter(book=book, reader=reader, return_date=None).exists():
                    return render(request, "all_books.html", {'user': user, 'books': books, 'form': book_form, 'error_message': f"Книга '{book.title}' уже выдана вам"})
                else:
                    book_loan = BookLoan(book=book, reader=reader)
                    book_loan.save()
                    book.is_visible = False
                    book.save()
                    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
            except Book.DoesNotExist:
                return render(request, "all_books.html", {'user': user, 'books': books, 'form': book_form, 'error_message': 'Книга не найдена'})
        else:
            return render(request, "all_books.html", {'user': user, 'books': books, 'form': book_form, 'error_message': 'Данные формы не валидны'})
    else:
        book_form = BookCode()
        return render(request, "all_books.html", {'user': user, 'books': books, 'form': book_form})

def book_loan_list_view(request):
    book_loans = BookLoan.objects.all()
    return render(request, 'book_loans.html', {'book_loans': book_loans})

