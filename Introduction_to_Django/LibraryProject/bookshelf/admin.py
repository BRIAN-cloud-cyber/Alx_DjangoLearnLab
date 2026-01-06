from django.contrib import admin
from .models import Book

class BookList(admin.ModelAdmin):
    list=["title","author","publication_year"]

admin.site.register(Book,BookList)
