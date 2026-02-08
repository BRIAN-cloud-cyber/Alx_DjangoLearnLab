from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView
)

urlpatterns = [
    path("books/", BookListView.as_view()),
    path("books/<int:pk>/", BookDetailView.as_view()),
    path("books/create/", BookCreateView.as_view()),
    path("books/<int:pk>/update/", BookUpdateView.as_view()),
    path("books/<int:pk>/delete/", BookDeleteView.as_view()),
]
