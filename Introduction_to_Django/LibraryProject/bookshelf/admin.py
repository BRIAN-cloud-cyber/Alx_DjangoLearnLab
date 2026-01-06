from django.contrib import admin
from .models import Book

class BookList(admin.ModelAdmin):
    list_filter=["title","author","publication_year"]
    search_fields=("author","title")

admin.site.register(Book,BookList)
