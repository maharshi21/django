# myapp/urls.py

from django.urls import path
from .views import item_create, item_delete, item_update, filter_data

urlpatterns = [
    path('items/create/', item_create, name='item-create'),
    path('items/delete/<int:item_id>', item_delete, name='item'),
    path('items/update/<int:item_id>', item_update, name='update'),
    path('items/filter/', filter_data, name='item-filter'),
]
