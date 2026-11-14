from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'
    def __str__(self): return self.name

class Unit(models.Model):
    name = models.CharField(max_length=80, unique=True)
    abbreviation = models.CharField(max_length=12, unique=True)
    is_active = models.BooleanField(default=True)
    class Meta: ordering = ['name']
    def __str__(self): return f'{self.name} ({self.abbreviation})'

class InventoryItem(models.Model):
    sku = models.CharField(max_length=40, unique=True, db_index=True)
    name = models.CharField(max_length=180)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='items')
    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, related_name='items')
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'), validators=[MinValueValidator(Decimal('0.00'))])
    quantity = models.PositiveIntegerField(default=0, help_text='Opening stock quantity; stock movements will be introduced in Week 3.')
    reorder_level = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ['name', 'sku']
    def __str__(self): return f'{self.sku} - {self.name}'
    @property
    def low_stock(self): return self.is_active and self.quantity <= self.reorder_level
    @property
    def stock_value(self): return self.quantity * self.unit_cost
