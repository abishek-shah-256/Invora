from django.contrib import admin
from .models import Category, Unit, InventoryItem
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=('name','is_active','created_at')
    search_fields=('name',)
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display=('name','abbreviation','is_active')
@admin.register(InventoryItem)
class ItemAdmin(admin.ModelAdmin):
    list_display=('sku','name','category','unit','quantity','reorder_level','is_active')
    search_fields=('sku','name')
    list_filter=('category','is_active')
