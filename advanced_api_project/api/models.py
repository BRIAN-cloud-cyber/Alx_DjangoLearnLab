from django.db import models

# Author model represents a writer who can have multiple books
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# Book model represents a published book linked to one author
class Book(models.Model):
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name="books",  # Enables reverse access: author.books.all()
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
