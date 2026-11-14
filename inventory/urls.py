from django.urls import path
from . import views
urlpatterns=[
    path('',views.overview,name='inventory_overview'),
    path('items/',views.item_list,name='inventory_item_list'),
    path('items/add/',views.item_create,name='inventory_item_create'),
    path('items/<int:pk>/edit/',views.item_edit,name='inventory_item_edit'),
    path('items/<int:pk>/status/',views.item_toggle,name='inventory_item_toggle'),
    path('categories/',views.category_list,name='inventory_categories'),
    path('categories/add/',views.category_form,name='inventory_category_add'),
    path('categories/<int:pk>/edit/',views.category_form,name='inventory_category_edit'),
    path('units/',views.unit_list,name='inventory_units'),
    path('units/add/',views.unit_form,name='inventory_unit_add'),
    path('units/<int:pk>/edit/',views.unit_form,name='inventory_unit_edit'),
]
