from django.conf import settings

from products.models import Category, PopupOffer
from web.cart import Cart


def main_context(request):
    all_categories = Category.objects.all()
    cart_instance = Cart(request)
    cart = cart_instance.cart
    cart_count = len(cart)
    popular_image = None
    if PopupOffer.objects.filter(is_active=True).exists():
        popular_image = PopupOffer.objects.filter(is_active=True).last()
    return {
        "all_categories": all_categories,
        "cart_count": cart_count,
        "domain": request.META["HTTP_HOST"],
        "current_version": "?v=2.0",
        "RAZOR_PAY_KEY": settings.RAZOR_PAY_KEY,
        "RAZOR_PAY_SECRET": settings.RAZOR_PAY_SECRET,
        "popular_image" : popular_image
    }
