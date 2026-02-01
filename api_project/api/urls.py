from django.urls import path
from .views import BookList

url_patterns=[
    path('books/',BookList.as_view,name='book-list')
]