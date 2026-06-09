from django.contrib import admin
from .models import User, Department, Add_Employee, Query, Item, Order, Cart

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Add_Employee)
admin.site.register(Query)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(Cart)