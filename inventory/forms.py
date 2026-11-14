from django import forms
from .models import Category, Unit, InventoryItem

class StyledModelForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, forms.CheckboxInput): field.widget.attrs['class']='form-check-input'
            else: field.widget.attrs['class']='form-select' if isinstance(field.widget, forms.Select) else 'form-control'

class CategoryForm(StyledModelForm):
    class Meta:
        model=Category
        fields=['name','description','is_active']
        widgets={'description':forms.Textarea(attrs={'rows':3})}

class UnitForm(StyledModelForm):
    class Meta:
        model=Unit
        fields=['name','abbreviation','is_active']

class ItemForm(StyledModelForm):
    class Meta:
        model=InventoryItem
        fields=['sku','name','description','category','unit','unit_cost','quantity','reorder_level','is_active']
        widgets={'description':forms.Textarea(attrs={'rows':3})}
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        if not self.instance.pk:
            self.fields['category'].queryset=Category.objects.filter(is_active=True)
            self.fields['unit'].queryset=Unit.objects.filter(is_active=True)
        else:
            self.fields['category'].queryset=Category.objects.filter(is_active=True) | Category.objects.filter(pk=self.instance.category_id)
            self.fields['unit'].queryset=Unit.objects.filter(is_active=True) | Unit.objects.filter(pk=self.instance.unit_id)
        self.fields['quantity'].help_text='Opening balance only. Week 3 will introduce tracked stock transactions.'
    def clean_sku(self): return self.cleaned_data['sku'].strip().upper()
