from django.contrib import admin
from .models import Supplier_m

class SupplierAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(SupplierAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj:
            # Dans le cas où aucun objet spécifique n'est demandé
            return True
        return obj.user == request.user or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        if not obj:
            # Dans le cas où aucun objet spécifique n'est demandé
            return True
        return obj.user == request.user or request.user.is_superuser

admin.site.register(Supplier_m, SupplierAdmin)
