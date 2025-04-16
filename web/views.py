import urllib.parse
from decimal import Decimal
from django.utils import timezone
# PHONEPAY
import razorpay
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Min, Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView
from django.views.generic.detail import DetailView
from main.mixins import LoginRequiredMixin
import requests

# model
from web.models import Testimonial
from main.models import District,ShippingFee
from order.forms import OrderForm
from order.models import Order, OrderItem
from products.forms import ReviewForm
from products.models import AvailableSize, Category, Offer, Product, Slider, Tag, PopupOffer,Wishlist

# CART
from web.cart import Cart

# form
from web.forms import ContactForm

client = razorpay.Client(auth=(settings.RAZOR_PAY_KEY, settings.RAZOR_PAY_SECRET))


class IndexView(TemplateView):
    template_name = "web/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        instances = Product.objects.filter(is_active=True)
        products = Product.objects.all()

        context["categories"] = categories
        context["products"] = products
        context["popular_products"] = instances.filter(is_popular=True)
        context["best_seller_products"] = instances.filter(is_best_seller=True)
        context["offers"] = Offer.objects.all()
        context["sliders"] = Slider.objects.filter(is_active=True)
        context["testimonials"] = Testimonial.objects.all()

        # Add category products to context
        category_products = {category: category.get_products() for category in categories}
        context["category_products"] = category_products
        
        return context

class AboutView(TemplateView):
    template_name = "web/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["testimonials"] = Testimonial.objects.all()
        
        return context
    
    
class ShopView(ListView):
    model = Product
    template_name = "web/shop.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        products = Product.objects.filter(is_active=True)
        search_query = self.request.GET.get("search")
        category = self.request.GET.get("category")
        sort_by = self.request.GET.get("sort_by")
        price_range = self.request.GET.get("price-range")
        category_title = None

        if search_query:
            products = products.filter(Q(name__icontains=search_query))
        if category:
            category_title = Category.objects.get(slug=category)
            products = products.filter(category__slug=category)
        if sort_by:
            if sort_by == "low_to_high":
                annotated_queryset = products.annotate(
                    min_sale_price=Min("availablesize__sale_price")
                )
                products = annotated_queryset.order_by("min_sale_price")
            elif sort_by == "high_to_low":
                annotated_queryset = products.annotate(
                    min_sale_price=Min("availablesize__sale_price")
                )
                products = annotated_queryset.order_by("-min_sale_price")
            elif sort_by == "rating":
                products = products.order_by("-rating")
            else:
                products = products.order_by("-id")
        if price_range:
            amount = price_range.replace("₹", "")
            try:
                min_amount, max_amount = map(int, amount.split("-"))
                products = products.filter(
                    availablesize__sale_price__gte=min_amount,
                    availablesize__sale_price__lte=max_amount,
                ).distinct()
            except ValueError:
                print("ValueError")

        self.category_title = category_title if category_title else None
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["tags"] = Tag.objects.all()
        context["title"] = self.category_title
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = "web/product_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_product = self.get_object()
        related_products = Product.objects.filter(
            category=current_product.category
        ).exclude(pk=current_product.pk)[:12]
        product_ratings = [
            {"value": 5, "percentage": int(current_product.five_rating())},
            {"value": 4, "percentage": int(current_product.four_rating())},
            {"value": 3, "percentage": int(current_product.three_rating())},
            {"value": 2, "percentage": int(current_product.two_rating())},
            {"value": 1, "percentage": int(current_product.one_rating())},
        ]
        context["related_products"] = related_products
        context["reviews"] = (current_product.reviews.filter(approval=True),)
        context["review_form"] = ReviewForm()
        context["product_ratings"] = product_ratings
        return context

    def post(self, request, *args, **kwargs):
        product = self.get_object()
        form = ReviewForm(request.POST)

        if form.is_valid():
            form.instance.product = product
            form.save()
            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Message successfully Submitted",
            }
        else:
            print(form.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
                "message": form.errors,
            }
        return JsonResponse(response_data)


class ContactView(View):
    def get(self, request):
        # Empty form is rendered when the page is first visited
        form = ContactForm()
        context = {
            "is_contact": True,
            "form": form,
        }
        return render(request, "web/contact.html", context)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact form data
            contact = form.save()

            # Send email to the owner
            subject = f"New message from {contact.first_name} {contact.last_name}"
            message = f"""
            You have received a new contact form submission:

            Name: {contact.first_name} {contact.last_name}
            Email: {contact.email}
            Phone: {contact.phone}
            Subject: {contact.subject}

            Message:
            {contact.message}
            """
            from_email = contact.email  # The email of the person submitting the form
            recipient_email = settings.OWNER_EMAIL  # Owner's email, set this in settings.py

            try:
                send_mail(subject, message, from_email, [recipient_email])

                # Return success response for frontend and reload the form
                return render(request, "web/contact.html", {
                    "form": ContactForm(),
                    "success_message": "Your message has been sent successfully!"
                })
            except Exception as e:
                # In case of any error in sending the email
                return render(request, "web/contact.html", {
                    "form": ContactForm(),
                    "error_message": f"An error occurred while sending the email: {str(e)}"
                })

        else:
            # If the form is not valid, we will show the errors
            return render(request, "web/contact.html", {
                "form": form,
                "error_message": "There were some errors with your submission. Please check the form and try again."
            })


# CART
def cart_view(request):
    cart = Cart(request)
    cart_items = []

    for item_id, item_data in cart.get_cart():
        variant = get_object_or_404(AvailableSize, id=item_id)
        quantity = item_data["quantity"]
        total_price = Decimal(item_data["sale_price"]) * quantity
        cart_items.append(
            {
                "product": variant,
                "quantity": quantity,
                "total_price": total_price,
            }
        )
    context = {
        "cart_items": cart_items,
        "cart_total": sum(
            Decimal(item[1]["quantity"]) * Decimal(item[1]["sale_price"])
            for item in cart.get_cart()
        ),
    }

    return render(request, "web/cart.html", context)


def cart_add(request):
    cart = Cart(request)
    cart_instance = cart.cart
    quantity = request.GET.get("quantity", 1)
    product_id = request.GET.get("product_id", "")
    print('product_id=',product_id)
    variant = get_object_or_404(AvailableSize, pk=product_id)
    cart.add(variant, quantity=int(quantity))
    return JsonResponse(
        {
            "message": "Product Quantity Added from cart successfully",
            "quantity": cart.get_product_quantity(variant),
            "total_price": cart.get_total_price(cart_instance[product_id]),
            "cart_total": cart.cart_total(),
            "cart_count": len(cart_instance),
        }
    )


def clear_cart_item(request, item_id):
    cart = Cart(request)
    variant = get_object_or_404(AvailableSize, id=item_id)
    cart.remove(variant)
    return redirect(reverse("web:cart"))


def minus_to_cart(request):
    cart = Cart(request)
    cart_instance = cart.cart
    item_id = request.GET.get("item_id")
    variant = get_object_or_404(AvailableSize, id=item_id)
    cart.decrease_quantity(variant)
    return JsonResponse(
        {
            "message": "Product Quantity decreased from cart successfully",
            "quantity": cart.get_product_quantity(variant),
            "total_price": cart.get_total_price(cart_instance[item_id]),
            "cart_total": cart.cart_total(),
        }
    )


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect(reverse("web:shop"))


def order(request):
    if request.method == "POST":
        cart = Cart(request)
        products = ""
        total = 0
        counter = 1
        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(AvailableSize, id=item_id)
            quantity = item_data["quantity"]
            price = Decimal(item_data["sale_price"])
            if variant.product.category.is_combo:
                products += f"{counter}.{variant.product.name} ({quantity}x{price}) ₹ {variant.weight*quantity} \n ----------------------- \n"
            else:
                products += f"{counter}.{variant.product.name}-{variant.weight} {variant.unit} ({quantity}x{price}) ₹ {variant.sale_price*quantity} \n ----------------------- \n"
            total += quantity * variant.sale_price
            counter += 1

        message = (
            f"============================\n"
            f"Welcome to keralathengu.\n"
            f"============================\n\n"
            f'Name: {request.POST.get("name")}\n'
            f'Phone: {request.POST.get("phone")}\n'
            f'Address: {request.POST.get("address")}\n'
            f"----------------------------\n\n"
            f"Products:\n"
            f"{products}\n\n"
            f"Grand Total: {total}\n"
            f"============================\n"
            f"Thank you for placing your order with keralathengu. Your order has been confirmed.your order will be delivered in 7 working days.\n"
            f"Thank you for shopping with us.\n "
        )

        whatsapp_api_url = "https://api.whatsapp.com/send"
        phone_number = "917593973478"
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"{whatsapp_api_url}?phone={phone_number}&text={encoded_message}"
        cart.clear()
        return redirect(whatsapp_url)


class CheckoutView(LoginRequiredMixin, View):
    template_name = "web/shop-checkout.html"

    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        form = OrderForm()
        shipping_options = ShippingFee.objects.all().last()

        context = {
            "cart_items": cart_items,
            "cart_total": sum(item["total_price"] for item in cart_items),
            "form": form,
            "shipping_options": shipping_options,
            "turnstile_site_key": settings.CLOUDFLARE_TURNSTILE_PUBLIC_KEY,
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST)
        cart = Cart(request)
        cart_items = self.get_cart_items(cart)
        
        # CAPTCHA Verification
        turnstile_response = request.POST.get('cf-turnstile-response')
        data = {
            'secret': settings.CLOUDFLARE_TURNSTILE_PRIVATE_KEY,
            'response': turnstile_response,
        }
        captcha_response = requests.post('https://challenges.cloudflare.com/turnstile/v0/siteverify', data=data)
        captcha_result = captcha_response.json()

        if not captcha_result.get('success'):
            return JsonResponse({
                "status": "false",
                "title": "CAPTCHA verification failed",
                "message": "Please complete the CAPTCHA correctly."
            })

        if form.is_valid():
            selected_dial_code_mobile = form.cleaned_data.get("selected_dial_code_mobile")
            selected_dial_code_alternative = form.cleaned_data.get("selected_dial_code_alternative")
            m_n = form.cleaned_data.get("mobile_no")
            a_n = form.cleaned_data.get("alternative_no")
            mobile_no = f"{selected_dial_code_mobile}{m_n}"
            alternative_no = f"{selected_dial_code_alternative}{a_n}"

            # Save Order
            data = form.save(commit=False)
            data.user = request.user  # Assign logged-in user
            data.subtotal = request.POST.get("payable")
            data.service_fee = request.POST.get("service_fee")
            data.shipping_fee = request.POST.get("shipping_fee")
            data.payable = request.POST.get("total_amt")
            data.payment_method = request.POST.get("selected_payment")
            data.mobile_no = mobile_no
            data.alternative_no = alternative_no
            data.save()

            # Save Order Items
            for item_id, item_data in cart.get_cart():
                variant = get_object_or_404(AvailableSize, id=item_id)
                quantity = item_data["quantity"]
                price = Decimal(item_data["sale_price"])
                order_item = OrderItem.objects.create(
                    order=data,
                    product=variant,
                    price=price,
                    quantity=quantity,
                )
                order_item.save()

            # Redirect based on payment method
            if data.payment_method == "OP":
                return redirect("web:payment", pk=data.pk)
            else:
                return redirect("web:complete_order", pk=data.pk)
        
        else:
            context = {
                "cart_items": cart_items,
                "cart_total": sum(item["total_price"] for item in cart_items),
                "form": form,
            }
            return render(request, self.template_name, context)

    def get_cart_items(self, cart):
        cart_items = []
        for item_id, item_data in cart.get_cart():
            variant = get_object_or_404(AvailableSize, id=item_id)
            quantity = item_data["quantity"]
            total_price = Decimal(item_data["sale_price"]) * quantity
            cart_items.append({
                "variant": variant,
                "quantity": quantity,
                "total_price": total_price,
            })
        return cart_items

    

class PaymentView(View):
    def get(self, request, pk, *args, **kwargs):
        order = get_object_or_404(Order, pk=pk)
        currency = "INR"
        amount = float(order.payable) * 100
        razorpay_order = client.order.create(
            {"amount": amount, "currency": currency, "payment_capture": "1"}
        )
        razorpay_order_id = razorpay_order["id"]
        order.razorpay_order_id = razorpay_order_id
        order.save()
        context = {
            "object": order,
            "amount": amount,
            "razorpay_key": settings.RAZOR_PAY_KEY,
            "razorpay_order_id": razorpay_order_id,
            "callback_url": f"{settings.DOMAIN}/callback/{order.pk}/",
        }
        return render(request, "web/payment.html", context=context)


@csrf_exempt
def callback(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        response_data = {
            "razorpay_order_id": provider_order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature_id,
        }

        order = Order.objects.get(razorpay_order_id=provider_order_id)
        order.razorpay_payment_id = payment_id
        order.razorpay_signature = signature_id
        client = razorpay.Client(
            auth=(settings.RAZOR_PAY_KEY, settings.RAZOR_PAY_SECRET)
        )
        result = client.utility.verify_payment_signature(response_data)

        if result is not None:
            print("Signature verification successful")
            order.is_ordered = True
            order.order_status = "Placed"
            order.payment_status = "Success"
            order.save()

            products = ""
            total = 0
            counter = 1
            for item in order.get_items():
                
                products += f"{counter}.{item.product.product.name}-{item.product.weight} {item.product.unit} ({item.quantity}x{item.price}) ₹ {item.subtotal()} \n ----------------------- \n"
                total += item.subtotal()
                counter += 1

            message = (
                f"============================\n"
                f"Order Confirmed\n"
                f"============================\n\n"
                f"Order ID: {order.order_id}\n"
                f"Order Date: {order.created}\n"
                f"Order Status: Placed\n"
                f"Payment Method: Online Payment\n"
                f"Payment Status: Success\n"
                f"----------------------------\n\n"
                f"Products:\n\n"
                f"{products}\n\n"
                f"----------------------------\n\n"
                f"Order Summary:\n\n"
                f"Subtotal: {order.subtotal} \n"
                f"service fee: {order.service_fee} \n"
                f"shipping fee: {order.shipping_fee} \n\n"
                f"Total Payble: {order.payable} \n\n"
                f"----------------------------\n\n"
                f"Shipping Address:\n\n"
                f"Name: {order.full_name}\n"
                f"Address: {order.address_line_1}\n"
                f"Landmark: {order.address_line_2}\n"
                f"State: {order.state}\n"
                f"District: {order.district}\n"
                f"City: {order.city}\n"
                f"Pincode: {order.pin_code}\n"
                f"Mobile: {order.mobile_no}\n"
                f"Email: {order.email}\n\n"
                f"Thank you for placing your order with keralathengu. Your order has been confirmed.your order will be delivered in 7 working days.\n\n"
            )

            email = order.email
            subject = "Order Confirmation - keralathengu"
            message = message
            send_mail(
                subject,
                message,
                "secure.gedexo@gmail.com",
                [email,"info@keralathengu.com"],
                fail_silently=False,
            )
            
            print("email sent successfully")
            cart = Cart(request)
            cart.clear()
            
        else:
            print("Signature verification failed, please check the secret key")
            order.payment_status = "Failed"
            order.save()
        return render(request, "web/callback.html", {"object": order})
    else:
        print("Razorpay payment failed")
        return redirect("web:payment", pk=order.pk)


class CompleteOrderView(DetailView):
    model = Order
    template_name = "web/complete-order.html"

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        order.is_ordered = True
        order.order_status = "Placed"
        order.save()
        products = ""
        total = 0
        counter = 1
        for item in order.get_items():
            products += f"{counter}.{item.product.product.name}-{item.product.weight} {item.product.unit} ({item.quantity}x{item.price}) ₹ {item.subtotal()} \n ----------------------- \n"
            total += item.subtotal()
            counter += 1

        message = (
            f"============================\n"
            f"Order Confirmed\n"
            f"============================\n\n"
            f"Order ID: {order.order_id}\n"
            f"Order Date: {order.created}\n"
            f"Order Status: Placed\n"
            f"Payment Method: Cash On Delivery\n"
            f"Payment Status: Pending\n"
            f"----------------------------\n"
            f"Products:\n\n"
            f"{products}\n"
            f"----------------------------\n"
            f"Order Summary:\n\n"
            f"Subtotal: {order.subtotal} \n"
            f"service fee: {order.service_fee} \n"
            f"shipping fee: {order.shipping_fee} \n\n"
            f"Total Payble: {order.payable} \n\n"
            f"----------------------------\n"
            f"Shipping Address:\n\n"
            f"Name: {order.full_name}\n"
            f"Address: {order.address_line_1}\n"
            f"Landmark: {order.address_line_2}\n"
            f"State: {order.state}\n"
            f"District: {order.district}\n"
            f"City: {order.city}\n"
            f"Pincode: {order.pin_code}\n"
            f"Mobile: {order.mobile_no}\n"
            f"Email: {order.email}\n\n"
            f"Thank you for placing your order with keralathengu. Your order has been confirmed.your order will be delivered in 7 working days.\n\n"
        )

        email = order.email
        subject = "Order Confirmation - keralathengu"
        message = message
        send_mail(
            subject,
            message,
            "secure.gedexo@gmail.com",
            [email,"info@keralathengu.com"],
            fail_silently=False,
        )
        
        cart = Cart(request)
        cart.clear()
        context = {
            "object": order,
        }
        return render(request, self.template_name, context)

class UserOrderDetailView(DetailView):
    model = Order
    template_name = "account/order_single.html"
    context_object_name = "order"
    slug_field = "order_id"
    slug_url_kwarg = "order_id"
    extra_context = {"my_order": True}


def get_shipping_fee(request):
    district_id = request.GET.get("district", None)
    data = District.objects.get(id=district_id).delivery_charge
    return JsonResponse({"charge": data})


#wishlist

class WishlistListView(LoginRequiredMixin, ListView):
    model = Wishlist
    template_name = "web/wishlist.html"
    context_object_name = "wishlist_items"
    paginate_by = 10

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user)


class AddToWishlistView( View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'message': 'User not authenticated'}, status=401)
        user = self.request.user
        product_id = request.GET.get("product_id",'')
        product = get_object_or_404(Product, pk=product_id)
        if not Wishlist.objects.filter(user=user, product=product).exists():
            # Create a new Wishlist object
            Wishlist.objects.create(
                user=user,
                product=product
            )
            return JsonResponse({'message': 'Product Added from Wishlist successfully','wishlist_count':Wishlist.objects.filter(user=request.user).count()})
        else:
            return JsonResponse({'message': 'Product is already in the Wishlist.','alreadyInWishlist': True})


class RemoveFromWishlistView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        product_id = self.kwargs.get("product_id")
        user = self.request.user

        wishlist_item = get_object_or_404(Wishlist, user=user, id=product_id)
        wishlist_item.delete()

        return redirect("web:wishlist")



# class MyAccountView(LoginRequiredMixin, TemplateView):
#     template_name = "web/account_dashboard.html"

    

class MyOrderView(LoginRequiredMixin, View):
    template_name = "web/account_dashboard.html"
    def get(self, request):
        user = self.request.user
        context = {
            "orders": Order.objects.filter(user=user),
        }
        return render(request, self.template_name, context)
    
    
class MyOrderDetailsView(LoginRequiredMixin, DetailView):
    template_name = "web/order_details.html"
    model = Order
    context_object_name = 'order'


class AutocompleteView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('query', '')
        results = []
        if query:
            products = Product.objects.filter(name__icontains=query, is_active=True)[:10]
            results = [
                {
                    'name': product.name,
                    'url': product.get_absolute_url()
                }
                for product in products
            ]
        return JsonResponse(results, safe=False)
    

def custom_404(request, exception):
    return render(request, "web/404.html", status=404)

def error(request):
    context = {
    }
    return render(request, "web/404.html", context)