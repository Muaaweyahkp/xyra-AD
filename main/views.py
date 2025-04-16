from django.shortcuts import render

# Create your views here.
from datetime import datetime, timedelta

from django import forms

# models
from django.contrib.auth.models import User
from django.db.models.deletion import ProtectedError
from django.forms import inlineformset_factory
from django.forms.formsets import formset_factory
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View

# view
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

# forms
from main.forms import (
    AvailableSizeForm,
    CategoryForm,
    DistrictForm,
    OfferForm,
    PopupOfferForm,
    ProductForm,
    ProductImageForm,
    ReviewForm,
    ShippingFeeForm,
    SliderForm,
    StateForm,
    TagForm,
    TestimonialForm,
)
from main.mixins import LoginRequiredMixin, SuperAdminLoginRequiredMixin
from main.models import District, ShippingFee, State
from order.models import Order
from products.models import (
    AvailableSize,
    Category,
    Offer,
    PopupOffer,
    Product,
    ProductImage,
    Review,
    Slider,
    Tag,
)
from web.forms import ContactForm
from web.models import Contact, Testimonial


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"
    extra_context = {"is_dashbord": True}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        two_weeks_ago = datetime.now() - timedelta(weeks=2)
        context["last_two_week_orders_count"] = Order.objects.filter(created__gte=two_weeks_ago).count()
        context["last_two_week_reviews_count"] = Review.objects.filter(created_at__gte=two_weeks_ago).count()
        context["last_two_week_customers_count"] = User.objects.filter(date_joined__gte=two_weeks_ago).count()
        context["orders"] = Order.objects.filter(is_ordered=True).order_by("-id")[:100]
        context["customers"] = User.objects.order_by("-id")[:100]
        context["reviews"] = Review.objects.order_by("-id")[:100]
        return context


# order
class OrderView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/order/list.html"
    model = Order
    extra_context = {"is_order": True}

    def get_queryset(self):
        return self.model.objects.filter(is_ordered=True)


class OrderDetailView(SuperAdminLoginRequiredMixin, DetailView):
    model = Order
    template_name = "dashboard/order/single.html"
    context_object_name = "order"
    slug_field = "order_id"
    slug_url_kwarg = "order_id"
    extra_context = {"is_order": True}


class InvoiceView(SuperAdminLoginRequiredMixin, DetailView):
    model = Order
    template_name = "account/invoice.html"
    context_object_name = "order"
    slug_field = "order_id"
    slug_url_kwarg = "order_id"
    extra_context = {"is_order": True}


class OrderUpdateView(SuperAdminLoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        status = request.GET.get("status")
        pk = request.GET.get("pk")
        order = get_object_or_404(Order, pk=pk)
        order.order_status = status
        order.save()
        message = "Order status updated successfully"
        response_data = {
            "status": "true",
            "title": "Successfully Updated",
            "message": str(message),
            "reload": "true",
        }

        return JsonResponse(response_data)


# State
class StateListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/state/list.html"
    model = State
    extra_context = {"is_state": True}


class StateCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = State
    template_name = "dashboard/state/entry.html"
    form_class = StateForm
    success_url = reverse_lazy("main:states")
    extra_context = {"is_state": True, "title": "Add New State"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "State Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class StateUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = State
    template_name = "dashboard/state/entry.html"
    form_class = StateForm
    success_url = reverse_lazy("main:states")
    extra_context = {"is_state": True, "title": "State Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "State Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class StateDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = State
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:states")
    extra_context = {"is_state": True}


# District
class DistrictListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/district/list.html"
    model = District
    extra_context = {"is_district": True}


class DistrictCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = District
    template_name = "dashboard/district/entry.html"
    form_class = DistrictForm
    success_url = reverse_lazy("main:districts")
    extra_context = {"is_district": True, "title": "Add New District"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "District Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class DistrictUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = District
    template_name = "dashboard/district/entry.html"
    form_class = DistrictForm
    success_url = reverse_lazy("main:districts")
    extra_context = {"is_district": True, "title": "District Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "District Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class DistrictDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = District
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:districts")


# tag
class TagListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/tag/list.html"
    model = Tag
    extra_context = {"is_tag": True}


class TagCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Tag
    template_name = "dashboard/tag/entry.html"
    form_class = TagForm
    success_url = reverse_lazy("main:tags")
    extra_context = {"is_tag": True, "title": "Add New Tag"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Tag Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class TagUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Tag
    template_name = "dashboard/tag/entry.html"
    form_class = TagForm
    success_url = reverse_lazy("main:tags")
    extra_context = {"is_tag": True, "title": "Edit Tag"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Tag Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class TagDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Tag
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["related_products"] = Product.objects.filter(tag=self.object)
        return context

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            error_message = "Cannot delete the object because it is referenced through protected foreign keys."
            return JsonResponse({"error": error_message}, status=400)


# category
class CategoryListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/category/list.html"
    model = Category
    extra_context = {"is_category": True, "is_category_list": True}


class CategoryCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Category
    template_name = "dashboard/category/entry.html"
    form_class = CategoryForm
    success_url = reverse_lazy("main:categories")
    extra_context = {
        "is_category": True,
        "is_category_create": True,
        "title": "Add New Category",
    }

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Category Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class CategoryUpdate(SuperAdminLoginRequiredMixin, UpdateView):
    model = Category
    template_name = "dashboard/category/entry.html"
    form_class = CategoryForm
    success_url = reverse_lazy("main:categories")
    extra_context = {"is_category": True, "is_edit": True, "title": "Edit Category"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Category Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class CategoryDelete(SuperAdminLoginRequiredMixin, DeleteView):
    model = Category
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:categories")
    extra_context = {"is_category": True}


# product
class ProductListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/product/list.html"
    model = Product
    extra_context = {"is_product": True, "is_product_list": True}


class CreateProductView(SuperAdminLoginRequiredMixin, View):
    template_name = "dashboard/product/entry.html"
    form_class = ProductForm
    available_size_formset_class = formset_factory(AvailableSizeForm, extra=1, can_delete=True)
    product_image_formset_class = formset_factory(ProductImageForm, extra=2, can_delete=True)

    def get(self, request, *args, **kwargs):
        available_size_formset = self.available_size_formset_class(prefix="available_size_formset")
        product_image_formset = self.product_image_formset_class(prefix="product_image_formset")
        product_form = self.form_class()
        context = {
            "is_product": True,
            "is_product_create": True,
            "title": "Add New Product",
            "available_size_formset": available_size_formset,
            "product_image_formset": product_image_formset,
            "form": product_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        product_image_formset = self.product_image_formset_class(request.POST, request.FILES, prefix="product_image_formset")
        available_size_formset = self.available_size_formset_class(request.POST, prefix="available_size_formset")
        product_form = self.form_class(request.POST, request.FILES)

        if available_size_formset.is_valid() and product_form.is_valid() and product_image_formset.is_valid():
            product = product_form.save()

            for size_form in available_size_formset:
                size_data = size_form.save(commit=False)
                size_data.product = product
                size_data.save()

            for image_form in product_image_formset:
                image_data = image_form.save(commit=False)
                image_data.product = product
                image_data.save()

            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Product Created successfully.",
            }
            return JsonResponse(response_data)
        else:
            message = ""
            if product_form.errors:
                message += str(product_form.errors)
            if available_size_formset.errors:
                message += str(available_size_formset.errors)
            if product_image_formset.errors:
                message += str(product_image_formset.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
                "message": message,
            }
            return JsonResponse(response_data)


def edit_product(request, pk):
    instance = get_object_or_404(Product.objects.filter(pk=pk))
    if ProductImage.objects.filter(product=instance).exists():
        extra = 0
    else:
        extra = 1

    ProductImageFormSet = inlineformset_factory(
        Product,
        ProductImage,
        can_delete=True,
        extra=extra,
        fields=("image",),
        widgets={
            "image": forms.FileInput(attrs={"class": "file-input required", "type": "file"}),
        },
    )
    if AvailableSize.objects.filter(product=instance).exists():
        extra = 0
    else:
        extra = 1

    AvailableSizeFormSet = inlineformset_factory(
        Product,
        AvailableSize,
        can_delete=True,
        extra=extra,
        fields="__all__",
        widgets={
            "weight": forms.TextInput(
                attrs={
                    "required": True,
                    "placeholder": "Weight",
                    "class": "required form-control",
                    "type": "number",
                }
            ),
            "unit": forms.Select(attrs={"class": "required form-select", "required": True}),
            "sale_price": forms.TextInput(
                attrs={
                    "placeholder": "Sale Price ",
                    "class": "required form-control",
                    "type": "number",
                    "required": True,
                }
            ),
            "regular_price": forms.TextInput(
                attrs={
                    "placeholder": "Regular Price ",
                    "class": "required form-control",
                    "type": "number",
                    "required": True,
                }
            ),
            "is_stock": forms.CheckboxInput(
                attrs={
                    "class": "form-check-input required",
                    "role": "switch",
                    "type": "checkbox",
                }
            ),
        },
    )

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=instance)
        product_image_formset = ProductImageFormSet(
            request.POST,
            request.FILES,
            prefix="product_image_formset",
            instance=instance,
        )
        available_size_formset = AvailableSizeFormSet(request.POST, prefix="available_size_formset", instance=instance)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            if product_image_formset.is_valid():
                ProductImage.objects.filter(product=data.pk).delete()
                for f1 in product_image_formset:
                    print(f1)
                    data1 = f1.save(commit=False)
                    data1.product = data
                    data1.save()

            if available_size_formset.is_valid():
                AvailableSize.objects.filter(product=data.pk).delete()
                for f0 in available_size_formset:
                    data2 = f0.save(commit=False)
                    data2.product = data
                    data2.save()

            response_data = {
                "status": "true",
                "title": "Successfully Submitted",
                "message": "Product Updated successfully.",
            }
            return JsonResponse(response_data)

        else:
            message = ""
            if form.errors:
                message += str(form.errors)
            if available_size_formset.errors:
                message += str(available_size_formset.errors)
            if product_image_formset.errors:
                message += str(product_image_formset.errors)
            response_data = {
                "status": "false",
                "title": "Form validation error",
                "message": message,
            }
            return JsonResponse(response_data)
    else:
        form = ProductForm(instance=instance)
        product_image_formset = ProductImageFormSet(prefix="product_image_formset", instance=instance)
        available_size_formset = AvailableSizeFormSet(prefix="available_size_formset", instance=instance)
        context = {
            "form": form,
            "product": instance,
            "title": "Edit Product",
            "is_edit": True,
            "product_image_formset": product_image_formset,
            "available_size_formset": available_size_formset,
        }
        return render(request, "dashboard/product/entry.html", context)


class ProductDelete(SuperAdminLoginRequiredMixin, DeleteView):
    model = Product
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:product_list")
    extra_context = {"is_product": True}


# customer
class CustomerListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/customer/list.html"
    model = User
    extra_context = {"is_customer": True}


# review
class ReviewListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/review/list.html"
    model = Review
    extra_context = {"is_review": True}


class ReviewCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Review
    template_name = "dashboard/review/entry.html"
    form_class = ReviewForm
    success_url = reverse_lazy("main:review_list")
    extra_context = {"is_review": True, "title": "Add New Review"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Review Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ReviewUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Review
    template_name = "dashboard/review/entry.html"
    form_class = ReviewForm
    success_url = reverse_lazy("main:review_list")
    extra_context = {"is_review": True, "title": "Edit Review"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Review Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ReviewDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Review
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:review_list")


# Slider


class SliderListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/slider/list.html"
    model = Slider
    extra_context = {"is_slider": True}


class SliderCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Slider
    template_name = "dashboard/slider/entry.html"
    form_class = SliderForm
    success_url = reverse_lazy("main:sliders")
    extra_context = {"is_slider": True, "title": "Add New Slider"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Slider Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class SliderUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Slider
    template_name = "dashboard/slider/entry.html"
    form_class = SliderForm
    success_url = reverse_lazy("main:sliders")
    extra_context = {"is_slider": True, "title": "Slider Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Slider Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class SliderDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Slider
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:sliders")


# offer


class OfferListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/offer/list.html"
    model = Offer
    extra_context = {"is_offer": True}


class OfferCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Offer
    template_name = "dashboard/offer/entry.html"
    form_class = OfferForm
    success_url = reverse_lazy("main:offers")
    extra_context = {"is_offer": True, "title": "Add New Offer"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Offer Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class OfferUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Offer
    template_name = "dashboard/offer/entry.html"
    form_class = OfferForm
    success_url = reverse_lazy("main:offers")
    extra_context = {"is_offer": True, "title": "Offer Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Offer Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class OfferDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Offer
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:offers")


# popupoffer


class PopupOfferListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/popupoffer/list.html"
    model = PopupOffer
    extra_context = {"is_popupoffer": True}


class PopupOfferCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Offer
    template_name = "dashboard/popupoffer/entry.html"
    form_class = PopupOfferForm
    success_url = reverse_lazy("main:popupoffers")
    extra_context = {"is_offer": True, "title": "Add New Popup Offer"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Popup Offer Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class PopupOfferUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = PopupOffer
    template_name = "dashboard/popupoffer/entry.html"
    form_class = PopupOfferForm
    success_url = reverse_lazy("main:popupoffers")
    extra_context = {"is_popupoffer": True, "title": "Popup Offer Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Popup Offer Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class PopupOfferDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = PopupOffer
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:popupoffers")


# Shipping Fee


class ShippingListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/shipping/list.html"
    model = ShippingFee
    extra_context = {"is_shipping": True}


class ShippingCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = ShippingFee
    template_name = "dashboard/shipping/entry.html"
    form_class = ShippingFeeForm
    success_url = reverse_lazy("main:shippingfees")
    extra_context = {"is_shipping": True, "title": "Add New Shipping Fee"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Shipping Fee Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ShippingUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = ShippingFee
    template_name = "dashboard/shipping/entry.html"
    form_class = ShippingFeeForm
    success_url = reverse_lazy("main:shippingfees")
    extra_context = {"is_shipping": True, "title": "Shipping Fee Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Shipping Fee Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ShippingDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = ShippingFee
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:shippingfees")


# contact
class ContactListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/contact/list.html"
    model = Contact
    extra_context = {"is_contact": True}


class ContactCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Contact
    template_name = "dashboard/contact/entry.html"
    form_class = ContactForm
    success_url = reverse_lazy("main:contacts")
    extra_context = {"is_contact": True, "title": "Add New Contact"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Contact Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ContactUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Contact
    template_name = "dashboard/contact/entry.html"
    form_class = ContactForm
    success_url = reverse_lazy("main:contacts")
    extra_context = {"is_contact": True, "title": "Contact Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Contact Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class ContactDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Contact
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:contact")


# testimonial


class TestimonialListView(SuperAdminLoginRequiredMixin, ListView):
    template_name = "dashboard/testimonial/list.html"
    model = Testimonial
    extra_context = {"is_testimonial": True}


class TestimonialCreateView(SuperAdminLoginRequiredMixin, CreateView):
    model = Testimonial
    template_name = "dashboard/testimonial/entry.html"
    form_class = TestimonialForm
    success_url = reverse_lazy("main:testimonials")
    extra_context = {"is_testimonial": True, "title": "Add New Testimonial"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Testimonial Created successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class TestimonialUpdateView(SuperAdminLoginRequiredMixin, UpdateView):
    model = Testimonial
    template_name = "dashboard/testimonial/entry.html"
    form_class = TestimonialForm
    success_url = reverse_lazy("main:testimonials")
    extra_context = {"is_testimonial": True, "title": "Testimonial Update"}

    def form_valid(self, form):
        response_data = super().form_valid(form)
        response_data = {
            "status": "true",
            "title": "Successfully Submitted",
            "message": "Testimonial Updated successfully.",
        }
        return JsonResponse(response_data)

    def form_invalid(self, form):
        response_data = super().form_invalid(form)
        response_data = {
            "status": "false",
            "title": "Form validation error",
            "message": str(form.errors),
        }
        return JsonResponse(response_data)


class TestimonialDeleteView(SuperAdminLoginRequiredMixin, DeleteView):
    model = Testimonial
    template_name = "dashboard/commen/delete.html"
    success_url = reverse_lazy("main:testimonials")
