from relationship_app.models import Author, Book, Library

# 1. Query all books by a specific author
author = Author.objects.get(name="John Doe")
books_by_author = Book.objects.filter(author=author)
print(books_by_author)

# 2. List all books in a library
library = Library.objects.get(name="Main Library")
print(library.books.all())

# 3. Retrieve the librarian for a library
print(library.librarian)
