from django.contrib import admin
from .models import *
from .modelcart import *
from django.contrib import admin

admin.site.register(Product_m)
admin.site.register(Order_m)
admin.site.register(OrderItem_m)
admin.site.register(Transaction)
admin.site.register(ProductBaseAnt_m)
admin.site.register(Ant_m)
admin.site.register(Pack_m)
admin.site.register(Nest_m)
admin.site.register(Size_m)
