from django import forms

from main.models import District, State,ShippingFee
from products.models import AvailableSize, Category, Product, ProductImage, Review, Tag,Slider,PopupOffer,Offer
from web.models import Testimonial

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = (
            "name",
            "image",
            "slug",
            "status",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Category Name", "class": "form-control"}
            ),
            "slug": forms.TextInput(
                attrs={"placeholder": "Category Slug", "class": "form-control"}
            ),
            "image": forms.FileInput(attrs={"class": "file-input"}),
            "status": forms.Select(attrs={"class": "form-select"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Product Name", "class": "form-control"}
            ),
            "slug": forms.TextInput(
                attrs={"placeholder": "Product Slug", "class": "form-control"}
            ),
            "details": forms.Textarea(attrs={"cols": "30", "rows": "10"}),
            "meta_title": forms.TextInput(
                attrs={"placeholder": "Title", "class": "form-control"}
            ),
            "meta_description": forms.Textarea(
                attrs={"placeholder": "Description", "class": "form-control", "rows": 3}
            ),
            "image": forms.FileInput(attrs={"class": "file-input"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "rating": forms.TextInput(
                attrs={
                    "placeholder": "Product Rating ",
                    "class": "form-control",
                    "type": "number",
                    "max": 5,
                    "min": 1,
                }
            ),
        }


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = (
            "name",
            "background_color",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Tag Name", "class": "form-control"}
            ),
            "background_color": forms.Select(attrs={"class": "form-select"}),
        }


class StateForm(forms.ModelForm):
    class Meta:
        model = State
        fields = (
            "name",
            "slug",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "State Name", "class": "form-control"}
            ),
            "slug": forms.TextInput(
                attrs={"placeholder": "State Slug", "class": "form-control"}
            ),
        }


class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = (
            "name",
            "slug",
            "state",
            "delivery_charge",
        )
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Enter District Name", "class": "form-control"}
            ),
            "slug": forms.TextInput(
                attrs={"placeholder": "District Slug", "class": "form-control"}
            ),
            "state": forms.Select(attrs={"class": "form-select"}),
            "delivery_charge": forms.TextInput(
                attrs={
                    "placeholder": "Delivery Charge ",
                    "class": "form-control",
                    "type": "number",
                }
            ),
        }


class AvailableSizeForm(forms.ModelForm):
    class Meta:
        model = AvailableSize
        fields = (
            "weight",
            "unit",
            "sale_price",
            "regular_price",
            "is_stock",
        )
        widgets = {
            "weight": forms.TextInput(
                attrs={
                    "required": True,
                    "placeholder": "Weight",
                    "class": "required form-control",
                    "type": "number",
                }
            ),
            "unit": forms.Select(
                attrs={"class": "required form-select", "required": True}
            ),
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
        }


class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ("image",)
        widgets = {
            "image": forms.FileInput(
                attrs={"class": "file-input required", "type": "file", "required": True}
            ),
        }


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [
        (1, "1 - Poor"),
        (2, "2 - Below Average"),
        (3, "3 - Average"),
        (4, "4 - Good"),
        (5, "5 - Excellent"),
    ]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES, widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Review
        exclude = ("created_at",)
        widgets = {
            "product": forms.Select(attrs={"class": "form-control"}),
            "fullname": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Your Full Name"}
            ),
            "headline": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "What’s most important to know",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "What did you like or dislike? What did you use this product for?",
                }
            ),
        }


class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ("title", "image", "description", "category", "is_active")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "file-input"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class PopupOfferForm(forms.ModelForm):
    class Meta:
        model = PopupOffer
        fields = ("image", "title", "description","category", "is_active")
        widgets = {
            "image": forms.FileInput(attrs={"class": "file-input"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        
class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ("image", "title", "discount_percentage", "category")
        widgets = {
            "image": forms.FileInput(attrs={"class": "file-input"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "discount_percentage": forms.TextInput(attrs={"class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }
        

class ShippingFeeForm(forms.ModelForm):
    class Meta:
        model = ShippingFee
        fields = ("name", "price")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.TextInput(attrs={"class": "form-control"}),
        }
        
        
class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ("name", "image","position", "description")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "file-input"}),
            "position": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control"}),
        }