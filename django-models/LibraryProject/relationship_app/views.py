from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library

# Function-based view
from django.shortcuts import render
from .models import Book
from . import forms
#from django.contrib import messages

# Function-based view
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


 
def register(request):
    if request.method == 'POST':
        form = forms.UserCreationForm(request.POST)
        if form.is_valid():
            #messages.success(request, 'Registration successful.')
            form.save()
            return render(request, 'relationship_app/registration_success.html')
    else:

        form = forms.UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

     