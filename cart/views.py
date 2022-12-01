import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from user.utils import get_respone
from user.utils import verify_token
from .models import Cart, CartItem, StatusChoice
from .serializers import CartSerializer

logger = logging.getLogger()


# Create your views here.
class CartViews(APIView):
    """
    Class to perform curd operation for the Cart
    """

    @swagger_auto_schema()
    @verify_token
    def get(self, request):
        """
        method to get the books inside the cartitem
        """
        try:
            print(request.data.get('user'))
            cart_list = Cart.objects.filter(user=request.data.get("user"), status=StatusChoice.NOT_PURCHASED)
            serializer = CartSerializer(cart_list, many=True)
            return get_respone(message="Book in the cartitem", data=serializer.data, status=200)

        except Exception as e:
            logger.exception(e)
            return get_respone(message="Something went Wrong", status=400)

    @swagger_auto_schema(request_body=CartSerializer)
    @verify_token
    def post(self, request):
        """
        method to perform the add operation to cart
        """
        try:

            serializer = CartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return get_respone(message=" Book Added to cart Successfully",
                               data=serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return get_respone(message=e.detail, status=204)

        except Exception as e:
            logger.exception(e)
            return get_respone(message="Something went Wrong", status=400)

    @swagger_auto_schema(request_body=CartSerializer)
    @verify_token
    def delete(self, request):
        """
        method to delate the books from the cart
        """
        try:
            cart = Cart.objects.get(user=request.data.get("user"), status=StatusChoice.NOT_PURCHASED)
            cartitem_count = CartItem.objects.filter(cart=cart.id)

            if cartitem_count.count() == 0:
                cart.delete()
                return get_respone(message="item in cart is successfully deleted", status=200)
            else:
                cart_item = cartitem_count
                for cartitem in cart_item:
                    cartitem.delete()
                    return get_respone(message="item in cartitem is successfully deleted", status=200)
        except Exception as e:
            logger.exception(e)
            return get_respone(message="Something went wrong", data=str(e), status=400)


@verify_token
def checkout_view(request):
    """
    method to update the purchase status of the user
    """
    cart = Cart.objects.filter(user=request.data.get("user"), status=StatusChoice.NOT_PURCHASED).first()

    if cart is not None:
        cart.status = StatusChoice.PUCHASED
        cart.save()
    return get_respone(message="successfully", status=200)


class WhistlistViews(APIView):
    """
    Class to perform curd operation for the whishlist
    """

    @verify_token
    def get(self, request):
        """
        method to get the books inside the whishlist
        """
        try:
            print(request.data.get('user'))
            cart_list = Cart.objects.filter(user=request.data.get("user"), status=StatusChoice.WISHLIST)
            serializer = CartSerializer(cart_list, many=True)
            return get_respone(message="Book in the cartitem", data=serializer.data, status=200)

        except Exception as e:
            logger.exception(e)
            return get_respone(message="Something went Wrong", status=400)

    @verify_token
    def post(self, request):
        """
        method to perform the add operation to whishlist
        """
        try:
            request.data.update(status=StatusChoice.WISHLIST)

            serializer = CartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return get_respone(message=" Book Added to cart Successfully",
                               data=serializer.data, status=status.HTTP_201_CREATED)

        except ValidationError as e:
            return get_respone(message=e.detail, status=204)

        except Exception as e:
            logger.exception(e)
            return get_respone(message="Something went Wrong", status=400)

    @verify_token
    def delete(self, request):
        """
        method to delate the books from the whishlist
        """
        try:
            cart = Cart.objects.get(user=request.data.get("user"), status=StatusChoice.WISHLIST)
            cartitem_count = CartItem.objects.filter(cart=cart.id)

            if cartitem_count.count() == 0:
                cart.delete()
                return get_respone(message="item in cart is successfully deleted", status=200)
            else:
                cart_item = cartitem_count
                for cartitem in cart_item:
                    cartitem.delete()
                    return get_respone(message="item in cartitem is successfully deleted", status=200)
        except Exception as e:
            logger.exception(e)
            return get_respone(message="Something went wrong", data=str(e), status=400)
