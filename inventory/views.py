from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Sum, F, DecimalField, ExpressionWrapper
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from accounts.decorators import role_required
from accounts.utils import log_action
from .models import Category, Unit, InventoryItem
from .forms import CategoryForm, UnitForm, ItemForm

CAN_EDIT=('inventory-officer','admin')

@login_required
def overview(request):
    items=InventoryItem.objects.filter(is_active=True).select_related('category','unit')
    low=items.filter(quantity__lte=F('reorder_level'))
    value=items.aggregate(total=Sum(ExpressionWrapper(F('quantity')*F('unit_cost'),output_field=DecimalField(max_digits=18,decimal_places=2))))['total'] or 0
    return render(request,'inventory/overview.html',{'item_count':items.count(),'category_count':Category.objects.filter(is_active=True).count(),'unit_count':Unit.objects.filter(is_active=True).count(),'low_count':low.count(),'low_items':low[:8],'stock_value':value,'recent_items':items.order_by('-created_at')[:8]})

@login_required
def item_list(request):
    items=InventoryItem.objects.select_related('category','unit')
    q=request.GET.get('q','').strip()
    category=request.GET.get('category','')
    status=request.GET.get('status','')
    if q: items=items.filter(Q(sku__icontains=q)|Q(name__icontains=q)|Q(description__icontains=q))
    if category.isdigit(): items=items.filter(category_id=int(category))
    if status=='low': items=items.filter(is_active=True,quantity__lte=F('reorder_level'))
    elif status=='active': items=items.filter(is_active=True)
    elif status=='inactive': items=items.filter(is_active=False)
    return render(request,'inventory/items.html',{'items':items,'categories':Category.objects.all(),'q':q,'category_filter':category,'status':status})

@role_required('inventory-officer')
def item_create(request):
    form=ItemForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        item=form.save();log_action(request,'CREATE','InventoryItem',item.pk,f'Created item {item.sku}')
        messages.success(request,'Inventory item created.');return redirect('inventory_item_list')
    return render(request,'inventory/form.html',{'form':form,'title':'Add inventory item','back_url':'inventory_item_list'})

@role_required('inventory-officer')
def item_edit(request,pk):
    item=get_object_or_404(InventoryItem,pk=pk)
    form=ItemForm(request.POST or None,instance=item)
    if request.method=='POST' and form.is_valid():
        form.save();log_action(request,'UPDATE','InventoryItem',item.pk,f'Updated item {item.sku}')
        messages.success(request,'Inventory item updated.');return redirect('inventory_item_list')
    return render(request,'inventory/form.html',{'form':form,'title':f'Edit {item.sku}','back_url':'inventory_item_list'})

@role_required('inventory-officer')
@require_POST
def item_toggle(request,pk):
    item=get_object_or_404(InventoryItem,pk=pk)
    item.is_active=not item.is_active;item.save(update_fields=['is_active','updated_at'])
    log_action(request,'STATUS_CHANGE','InventoryItem',item.pk,f'Item {item.sku} active={item.is_active}')
    messages.success(request,'Item status updated.');return redirect('inventory_item_list')

@login_required
def category_list(request): return render(request,'inventory/categories.html',{'categories':Category.objects.all()})

@role_required('inventory-officer')
def category_form(request,pk=None):
    obj=get_object_or_404(Category,pk=pk) if pk else None
    form=CategoryForm(request.POST or None,instance=obj)
    if request.method=='POST' and form.is_valid():
        saved=form.save();log_action(request,'UPDATE' if obj else 'CREATE','Category',saved.pk,saved.name)
        messages.success(request,'Category saved.');return redirect('inventory_categories')
    return render(request,'inventory/form.html',{'form':form,'title':'Edit category' if obj else 'Add category','back_url':'inventory_categories'})

@login_required
def unit_list(request): return render(request,'inventory/units.html',{'units':Unit.objects.all()})

@role_required('inventory-officer')
def unit_form(request,pk=None):
    obj=get_object_or_404(Unit,pk=pk) if pk else None
    form=UnitForm(request.POST or None,instance=obj)
    if request.method=='POST' and form.is_valid():
        saved=form.save();log_action(request,'UPDATE' if obj else 'CREATE','Unit',saved.pk,saved.name)
        messages.success(request,'Unit saved.');return redirect('inventory_units')
    return render(request,'inventory/form.html',{'form':form,'title':'Edit unit' if obj else 'Add unit','back_url':'inventory_units'})
