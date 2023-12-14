from django.db import models


class BookCategory(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)


class BookDetails(models.Model):
    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    genre = models.CharField(max_length=100)
    availability_status = models.BooleanField()
    category = models.ForeignKey(BookCategory, on_delete=models.CASCADE)
