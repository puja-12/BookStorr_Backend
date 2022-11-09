from django.db import models


class Book(models.Model):
    """
    model class for book model
    """
    title = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()


    def __str__(self):
        return self.title
