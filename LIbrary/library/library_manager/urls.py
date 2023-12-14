from django.urls import path
from .views import create_book, delete_book, update_book, filter_books

urlpatterns = [
    path('create/', create_book, name='create_book'),
    path('delete/<int:book_id>', delete_book, name='delete_book'),
    path('update/<int:book_id>', update_book, name='update_book'),
    path('filter/', filter_books, name='filter_books')
]
