from django.db import models

# Create your models here.
from django.core.validators import MaxValueValidator
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from versatileimagefield.fields import VersatileImageField
from django.contrib.auth.models import User
from main.models import COLOR_CHOICES, UNIT_CHOICES


class Slider(models.Model):
    title = models.CharField(max_length=255,blank=True,null=True)
    image = models.ImageField(upload_to="slider/")
    mobile_image = models.ImageField(upload_to="slider/",blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    category = models.ForeignKey("products.Category", on_delete=models.CASCADE,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    

    class Meta:
        verbose_name = _("Slider")
        verbose_name_plural = _("Sliders")
        ordering = ("title",)
    
    def get_list_url():
        return reverse_lazy("main:sliders")
    
    def get_update_url(self):
        return reverse_lazy("main:slider_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:slider_delete", kwargs={"pk": self.pk})
    
    def __str__(self):
        return str(self.title)


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    
    image = VersatileImageField(
        "category",
        blank=True,
        null=True,
        upload_to="categories/",
        help_text=" The recommended size is 120x120 pixels.",
    )
    status = models.CharField(
        max_length=20,
        choices=(("Published", "Published"), ("Unpublished", "Unpublished")),
        default="Published",
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        ordering = ("name",)

    def get_products(self):
        return Product.objects.filter(category=self)

    def get_product_count(self):
        return self.category.count()

    def __str__(self):
        return f"{self.name}"


class Tag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    background_color = models.CharField(
        max_length=10, choices=COLOR_CHOICES, default="success"
    )

    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    order = models.IntegerField(unique=True, blank=True,null=True)
    category = models.ForeignKey(
        "products.Category", on_delete=models.CASCADE, related_name="category"
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    # details = HTMLField(null=True, blank=True)
    details = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField(
        validators=[MaxValueValidator(5)],
        default=5,
        verbose_name="Product Rating(max:5)",
    )
    image = models.ImageField(
        upload_to="products/", help_text=" The recommended size is 220x220 pixels."
    )
    is_popular = models.BooleanField(default=False)
    is_best_seller = models.BooleanField(default=True)
    is_offer = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # meta
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=500, blank=True)

    class Meta:
        ordering = [
            "order",
        ]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    # def save(self, *args, **kwargs):
    #     if not self.image.name:
    #         unique_filename = f"keralathengu_{self.slug}_{uuid.uuid4()}.webp"
    #         self.image.name = os.path.join( unique_filename)
    #         super(Product, self).save(*args, **kwargs)

    def get_images(self):
        return ProductImage.objects.filter(product=self)

    def get_image(self):
        return ProductImage.objects.filter(product=self).first()

    def get_sizes(self):
        return AvailableSize.objects.filter(product=self, is_stock=True)

    def get_sale_price(self):
        return min([p.sale_price for p in self.get_sizes()])

    def get_regular_price(self):
        sizes = self.get_sizes()
        valid_prices = [p.regular_price for p in sizes if p.regular_price is not None]
        return min(valid_prices) if valid_prices else None

    def get_offer_percent_first(self):
        return self.get_sizes().first().offer_percent()

    def get_offer_percent(self):
        return min([p.offer_percent() for p in self.get_sizes()])

    def related_products(self):
        return Product.objects.filter().exclude(pk=self.pk).distinct()[0:12]

    def get_absolute_url(self):
        return reverse_lazy("web:product_detail", kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse_lazy("main:product_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:product_delete", kwargs={"pk": self.pk})

    def get_reviews(self):
        return Review.objects.filter(product=self, approval=True)

    def num_of_reviews(self):
        return self.get_reviews().count()

    def average_rating(self):
        from django.db.models import Avg

        return self.get_reviews().aggregate(Avg("rating"))["rating__avg"]

    def five_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=5).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=5).count()
            else 0
        )

    def four_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=4).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=4).count()
            else 0
        )

    def three_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=3).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=3).count()
            else 0
        )

    def two_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=2).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=2).count()
            else 0
        )

    def one_rating(self):
        return (
            round(
                (
                    self.get_reviews().filter(rating=1).count()
                    / self.get_reviews().count()
                )
                * 100
            )
            if self.get_reviews().filter(rating=1).count()
            else 0
        )

    def __str__(self):
        return f" {self.name}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="products/", help_text=" The recommended size is 800x600 pixels."
    )

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
        ordering = ("product",)

    def delete(self, *args, **kwargs):
        storage, path = self.image.storage, self.image.path
        super(ProductImage, self).delete(*args, **kwargs)
        storage.delete(path)


class AvailableSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField()
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    regular_price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    
    is_stock = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Available Size")
        verbose_name_plural = _("Available Sizes")
        ordering = ("sale_price",)

    def offer_percent(self):
        if self.regular_price and self.regular_price != self.sale_price:
            return ((self.regular_price - self.sale_price) / self.regular_price) * 100
        return 0

    # def save(self, *args, **kwargs):
    #     if self.regular_price is None:
    #         self.regular_price = self.sale_price
    #         super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("web:offer_details", kwargs={"pk": self.pk})
    
    def __str__(self):
        return f"{self.product} - {self.weight} {self.unit} "


class Offer(models.Model):
    title = models.CharField(max_length=200)
    image = VersatileImageField(
        blank=True,
        null=True,
        upload_to="Offers/",
        help_text=" The recommended size is 780x300 pixels.",
    )
    discount_percentage = models.CharField(max_length=200)
    category = models.ForeignKey("products.Category", on_delete=models.CASCADE,blank=True,null=True)

    def get_list_url():
        return reverse_lazy("main:offers")
    
    def get_update_url(self):
        return reverse_lazy("main:offer_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:offer_delete", kwargs={"pk": self.pk})
    
    def __str__(self):
        return str(self.title)


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveIntegerField(default=5)
    fullname = models.CharField(max_length=255)
    headline = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    approval = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.headline} - {self.product.name}"


class PopupOffer(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = VersatileImageField(
        blank=True,
        null=True,
        upload_to="Offers-popup/",
        help_text=" The recommended size is 400x460 pixels.",
    )
    category = models.ForeignKey("products.Category", on_delete=models.CASCADE,blank=True,null=True)

    is_active = models.BooleanField(default=True)

    def get_list_url():
        return reverse_lazy("main:popupoffers")
    
    def get_update_url(self):
        return reverse_lazy("main:popupoffer_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:popupoffer_delete", kwargs={"pk": self.pk})
    
    def __str__(self):
        return str(self.title)

   
class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.product}"