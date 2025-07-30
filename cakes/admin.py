from django.contrib import admin
from .models import Cake, Store, CartItem

admin.site.register(Cake)
admin.site.register(Store)
admin.site.register(CartItem)