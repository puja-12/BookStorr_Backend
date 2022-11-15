from django.urls import path
from cart import views

urlpatterns = [
    path('cart/', views.CartViews.as_view(), name="cart"),
    path('checkout/', views.checkout_view, name="checkout"),
    path('whistlist/', views.WhistlistViews.as_view(), name="whistlist")
]

