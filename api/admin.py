from django.contrib import admin
from store.models.stores import Store
from item.models.items import Item
from user.models.users import User

# Register your models here.
admin.site.register(Store)
admin.site.register(Item)
admin.site.register(User)