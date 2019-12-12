from django.contrib import admin
from .models import *
admin.site.register(Category)
admin.site.register(Post)
# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)