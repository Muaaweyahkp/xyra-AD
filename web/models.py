from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse_lazy


# Create your models here.


class Contact(models.Model):
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField()
    phone = models.CharField(
        max_length=15,
    )
    subject = models.CharField(
        max_length=120,
    )
    message = models.TextField()
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)

    def get_list_url():
        return reverse_lazy("main:contacts")
    
    def get_update_url(self):
        return reverse_lazy("main:contact_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:contact_delete", kwargs={"pk": self.pk})
    
    
    def __str__(self):
        return str(self.full_name())

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Testimonial(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="testimonials")
    position = models.CharField(max_length=120)
    description = models.TextField()
    timestamp = models.DateTimeField(db_index=True, auto_now_add=True)

    def get_list_url():
        return reverse_lazy("main:testimonials")
    
    def get_update_url(self):
        return reverse_lazy("main:testimonial_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:testimonial_delete", kwargs={"pk": self.pk})
    
    def __str__(self):
        return str(self.name)
