from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_id",'full_name','is_ordered', "payable", "order_status", "created",]
    list_filter = ["order_status", "created", "updated"]
    search_fields = ["order_id", "user__username"]
    inlines = (OrderItemInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request).all()
        return qs
    
