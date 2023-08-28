from django.contrib import admin
from django.db.models import Q

from .models import *
from .modelcart import *
from admin_supplier.models import Supplier_m
from django.contrib import admin

admin.site.register(Transaction)

@admin.register(Ant_m)
class AntAdmin(admin.ModelAdmin):
    list_display = ('localisation', 'spece', 'under_spece' )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        supplier = Supplier_m.objects.filter(user=request.user).first()
        if supplier:
            return qs.filter(supplier=supplier)
        return qs.none()

    def has_change_permission(self, request, obj=None):
        has_permission = super().has_change_permission(request, obj)
        if obj and not request.user.is_superuser:
            return obj.supplier.user == request.user and has_permission
        return has_permission

    def save_model(self, request, obj, form, change):
        """Automatiquement définir le fournisseur pour Other_m lors de la création."""
        if not change:  # Si c'est une nouvelle instance
            supplier = Supplier_m.objects.filter(user=request.user).first()
            if supplier:
                obj.supplier = supplier
        super().save_model(request, obj, form, change)

    def get_exclude(self, request, obj=None):
        excluded_fields = super().get_exclude(request, obj) or []
        if not request.user.is_superuser:  # Si ce n'est pas l'administrateur
            return excluded_fields + ['supplier']
        return excluded_fields


@admin.register(Size_m)
class SizeAdmin(admin.ModelAdmin):
    list_display = ('worker', 'gyne', 'stock', 'price', 'product_base',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:  # Si c'est l'administrateur
            return qs
        supplier = Supplier_m.objects.filter(user=request.user).first()
        if supplier:
            return qs.filter(supplier=supplier)
        return qs.none()  # Si ce n'est ni l'administrateur ni un fournisseur, ne rien montrer

    def has_change_permission(self, request, obj=None):
        has_permission = super().has_change_permission(request, obj)
        if obj and not request.user.is_superuser:
            return obj.supplier.user == request.user and has_permission
        return has_permission

    def get_exclude(self, request, obj=None):
        excluded_fields = super().get_exclude(request, obj) or []
        if not request.user.is_superuser:  # Si ce n'est pas l'administrateur
            return excluded_fields + ['supplier']
        return excluded_fields

    def save_model(self, request, obj, form, change):
        """Automatiquement définir le fournisseur pour Size_m lors de la création."""
        if not change:  # Si c'est une nouvelle instance
            supplier = Supplier_m.objects.filter(user=request.user).first()
            if supplier:
                obj.supplier = supplier
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "product_base":  # Si le champ est product_base
            supplier = Supplier_m.objects.filter(user=request.user).first()
            if supplier:
                kwargs["queryset"] = Ant_m.objects.filter(supplier=supplier)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Other_m)
class OtherAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock', 'price', 'type', )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        supplier = Supplier_m.objects.filter(user=request.user).first()
        if supplier:
            return qs.filter(supplier=supplier)
        return qs.none()

    def has_change_permission(self, request, obj=None):
        has_permission = super().has_change_permission(request, obj)
        if obj and not request.user.is_superuser:
            return obj.supplier.user == request.user and has_permission
        return has_permission

    def save_model(self, request, obj, form, change):
        """Automatiquement définir le fournisseur pour Other_m lors de la création."""
        if not change:  # Si c'est une nouvelle instance
            supplier = Supplier_m.objects.filter(user=request.user).first()
            if supplier:
                obj.supplier = supplier
        super().save_model(request, obj, form, change)

    def get_exclude(self, request, obj=None):
        excluded_fields = super().get_exclude(request, obj) or []
        if not request.user.is_superuser:  # Si ce n'est pas l'administrateur
            return excluded_fields + ['supplier']
        return excluded_fields

@admin.register(Pack_m)
class PackAdmin(admin.ModelAdmin):
    list_display = ('nest', 'price', 'size',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        supplier = Supplier_m.objects.filter(user=request.user).first()
        if supplier:
            return qs.filter(size__supplier=supplier)
        return qs.none()

    def has_change_permission(self, request, obj=None):
        has_permission = super().has_change_permission(request, obj)
        if obj and not request.user.is_superuser:
            return obj.size.supplier.user == request.user and has_permission
        return has_permission

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Restreindre les objets Size_m et Other_m pour Pack_m."""
        if db_field.name in ["nest", "size"]:
            supplier = Supplier_m.objects.filter(user=request.user).first()
            if supplier:
                if db_field.name == "nest":
                    kwargs["queryset"] = Other_m.objects.filter(supplier=supplier)
                else:
                    kwargs["queryset"] = Size_m.objects.filter(supplier=supplier)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(OrderItem_m)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_object', 'owner', 'quantity', 'is_ordered', 'date_added', 'price']
    ordering = ['-date_added']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        supplier = Supplier_m.objects.filter(user=request.user).first()
        if supplier:
            ant_ids = Ant_m.objects.filter(supplier=supplier).values_list('id', flat=True)
            other_ids = Other_m.objects.filter(supplier=supplier).values_list('id', flat=True)
            size_ids = Size_m.objects.filter(supplier=supplier).values_list('id', flat=True)
            pack_ids = Pack_m.objects.filter(size__in=size_ids).values_list('id', flat=True)

            # Filtrer les OrderItem_m par type et par identifiants récupérés précédemment
            return qs.filter(
                Q(content_type__model='ant_m', object_id__in=ant_ids) |
                Q(content_type__model='other_m', object_id__in=other_ids) |
                Q(content_type__model='pack_m', object_id__in=pack_ids)
            )
        return qs.none()

    def has_change_permission(self, request, obj=None):
        has_permission = super().has_change_permission(request, obj)
        if obj and not request.user.is_superuser:
            related_product = obj.content_object
            if hasattr(related_product, 'supplier'):
                return related_product.supplier.user == request.user and has_permission
        return has_permission

class Order_mAdmin(admin.ModelAdmin):
    list_display = ['id', 'ref_code', 'owner', 'is_ordered', 'date_ordered']
    ordering = ['-date_ordered']
admin.site.register(Order_m, Order_mAdmin)



@admin.register(OrderTrack_m)
class OrderTrackAdmin(admin.ModelAdmin):
    def get_orders_for_supplier(self, supplier):
        # Obtenir toutes les commandes qui contiennent au moins un produit du fournisseur
        order_ids = []
        for order in Order_m.objects.all():
            for item in order.items.all():
                if hasattr(item.content_object, 'supplier') and item.content_object.supplier == supplier:
                    order_ids.append(order.id)
                    break
        return Order_m.objects.filter(id__in=order_ids)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        supplier = Supplier_m.objects.filter(user=request.user).first()
        if supplier:
            return qs.filter(order__in=self.get_orders_for_supplier(supplier))
        return qs.none()

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "order":
            supplier = Supplier_m.objects.filter(user=request.user).first()
            if supplier:
                kwargs["queryset"] = self.get_orders_for_supplier(supplier)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


