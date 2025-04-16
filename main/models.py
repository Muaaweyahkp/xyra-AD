from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse, reverse_lazy

# CHOICES
GENDER_CHOICES = (("MALE", "Male"), ("FEMALE", "Female"), ("OTHER", "Other"))

COLOR_CHOICES = (
    ("danger", "red"),
    ("success", "Green"),
    ("info", "Blue"),
    ("warning", "Yellow"),
)

UNIT_CHOICES = (
    ("kg", "Kilogram"),
    ("pc", "Piece"),
    ("g", "Gram"),
    ("ltr", "Liter"),
    ("ml", "Milliliter"),
    ("m", "Meter"),
    ("cm", "Centimeter"),
)


class State(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return str(self.name)


class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return str(self.name)



class ShippingFee(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def get_list_url():
        return reverse_lazy("main:shippingfees")
    
    def get_update_url(self):
        return reverse_lazy("main:shippingfee_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:shippingfee_delete", kwargs={"pk": self.pk})
    
    def __str__(self):
        return str(self.name)