from django.db import models
from book.models import Book
from user.models import User


# Create your models here.
class StatusChoice(models.TextChoices):
    PUCHASED="purchased"
    WISHLIST="wishlist"
    NOT_PURCHASED= "not_purchased"

class Cart(models.Model):
    """
    model class for cart model
    """
    status = models.CharField(max_length=13,choices=StatusChoice.choices, default=StatusChoice.NOT_PURCHASED)
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



