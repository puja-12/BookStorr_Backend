from django.db import models
from book.models import Book
from user.models import User


# Create your models here.

class Cart(models.Model):
    """
    model class for cart model
    """
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class CartItem(models.Model):
    """
    model class to create the cartitem
    """
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)



