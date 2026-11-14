# Generated for Invora Week 2 inventory foundation.
from decimal import Decimal
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
import django.utils.timezone

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name='Category', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=100, unique=True)),
            ('description', models.TextField(blank=True)),
            ('is_active', models.BooleanField(default=True)),
            ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
        ], options={'ordering':['name'], 'verbose_name_plural':'Categories'}),
        migrations.CreateModel(name='Unit', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=80, unique=True)),
            ('abbreviation', models.CharField(max_length=12, unique=True)),
            ('is_active', models.BooleanField(default=True)),
        ], options={'ordering':['name']}),
        migrations.CreateModel(name='InventoryItem', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('sku', models.CharField(db_index=True, max_length=40, unique=True)),
            ('name', models.CharField(max_length=180)),
            ('description', models.TextField(blank=True)),
            ('unit_cost', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=12, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))])),
            ('quantity', models.PositiveIntegerField(default=0, help_text='Opening stock quantity; stock movements will be introduced in Week 3.')),
            ('reorder_level', models.PositiveIntegerField(default=0)),
            ('is_active', models.BooleanField(default=True)),
            ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ('updated_at', models.DateTimeField(auto_now=True)),
            ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='inventory.category')),
            ('unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='inventory.unit')),
        ], options={'ordering':['name','sku']}),
    ]
