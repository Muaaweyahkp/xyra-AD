from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import (
    AvailableSize,
    Category,
    Offer,
    Product,
    ProductImage,
    Review,
    Slider,
    PopupOffer,
)


@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "image_preview",
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = "Image Preview"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "image_preview", "status")
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("status",)
    search_fields = ("name",)
   

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = "Image Preview"


# @admin.register(Tag)
# class TagAdmin(admin.ModelAdmin):
#     list_display = ("name", "background_color")
#     search_fields = ("name",)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class AvailableSizeInline(admin.TabularInline):
    model = AvailableSize
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","order", "image_preview", "category", "is_active")
    exclude = ("creator",)
    list_filter = (
        "category",
        "is_best_seller",
        "is_offer",
    )
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    autocomplete_fields = ("category",)
    inlines = [ProductImageInline, AvailableSizeInline]

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    def sale_price(self, obj):
        return obj.get_sale_price()

    image_preview.short_description = "Image Preview"
    sale_price.short_description = "Sale Price"


@admin.register(AvailableSize)
class AvailableSizeAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "weight",
        "unit",
        "sale_price",
        "regular_price",
        "is_stock",
    )
    list_filter = ("product", "unit", "is_stock")


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("title", "image_preview", "category")

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = "Image Preview"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ["product", "rating", "approval", "created_at"]
    list_filter = ["approval", "created_at"]
    search_fields = ["headline", "content", "user__username", "product__title"]
    actions = ["approve_comments"]

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)

    approve_comments.short_description = "Approve selected comments"


@admin.register(PopupOffer)
class PopupOfferAdmin(admin.ModelAdmin):
    list_display = ("title", "image_preview", "category")

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(
                f'<img loading="lazy" src="{obj.image.url}" style="width:50px;height:50px;object-fit:contain;">'
            )
        return None

    image_preview.short_description = "Image Preview"


    

