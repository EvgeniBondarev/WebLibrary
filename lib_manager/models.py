from django.db import models

class Author(models.Model):
    """Модель для хранения информации об авторах."""
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, verbose_name="Отчество")

    class Meta:
        db_table = 'author'
        unique_together = ['first_name', 'last_name', 'middle_name']

class Reader(models.Model):
    """Модель для хранения информации о читателях."""
    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    middle_name = models.CharField(max_length=100, verbose_name="Отчество")

    class Meta:
        db_table = 'reader'
        unique_together = ['first_name', 'last_name', 'middle_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

class Book(models.Model):
    """Модель для хранения информации о книгах."""
    title = models.CharField(max_length=200, verbose_name="Название")
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    is_visible = models.BooleanField(default=True)

    class Meta:
        db_table = 'book'

class BookLoan(models.Model):
    """Модель для отслеживания выдачи и возврата книг читателями."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name="Читатель")
    loan_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата выдачи книги")
    return_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата возврата")

    class Meta:
        db_table = 'book_loan'