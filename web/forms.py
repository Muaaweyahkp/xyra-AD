from django import forms
from django.forms import widgets

from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        exclude = ("timestamp",)
        widgets = {
            "first_name": widgets.TextInput(attrs={"class": "required form-control", "placeholder": "Your First Name","required":True}),
            "last_name": widgets.TextInput(attrs={"class": "required form-control", "placeholder": "Your last Name","required":True}),
            "phone": widgets.TextInput(attrs={"class": "required form-control", "placeholder": "Your Phone","required":True}),
            "email": widgets.EmailInput(attrs={"class": "required form-control","placeholder": "Your Email Address","required":True}),
            "subject": widgets.TextInput(attrs={"class": "required form-control","placeholder": "Subject","required":True}),
            "message": widgets.Textarea(attrs={"class": "required form-control","cols":"30", "rows":"10","placeholder": "Type Your Message","required":True}),
        }