from django.contrib import admin
from .models import *
from .modelcart import *
from django.contrib import admin


class Order_mAdmin(admin.ModelAdmin):
    list_display = ['id', 'ref_code', 'owner', 'is_ordered', 'date_ordered']
    ordering = ['-date_ordered']



class OrderItem_mAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_object', 'owner', 'quantity', 'is_ordered', 'date_added', 'price']
    ordering = ['-date_added']

admin.site.register(OrderItem_m, OrderItem_mAdmin)
admin.site.register(Order_m, Order_mAdmin)

admin.site.register(Product_m)
admin.site.register(Transaction)
admin.site.register(Ant_m)
admin.site.register(Pack_m)
admin.site.register(Size_m)
admin.site.register(Other_m)
