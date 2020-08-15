from django.contrib import admin
from store.models.stores import Store
from item.models.items import Item

# Register your models here.
admin.site.register(Store)
admin.site.register(Item)