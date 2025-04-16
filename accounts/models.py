from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db import models

from main.models import GENDER_CHOICES

# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.PROTECT,
        limit_choices_to={"is_active": True},
        related_name="customer",
    )
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True
    )
    phone = models.CharField(max_length=15, blank=True, null=True)

    @property
    def fullname(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        else:
            return self.user

