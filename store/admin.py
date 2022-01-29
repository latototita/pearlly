from django.contrib import admin
from .models.product import Product
from .models.category import Category
from .models.orders import Order
from .models.brand import Brand



class AdminProduct(admin.ModelAdmin):
    list_display = ['name', 'price','stock', 'category','image','description']


class AdminBrand(admin.ModelAdmin):
    list_display = ['name']

class AdminCategory(admin.ModelAdmin):
    list_display = ['name']

class AdminOrder(admin.ModelAdmin):

    list_display = ['customer','product','price','quantity','address','phone','date','status','ordering_code']





# Register your models here.
admin.site.register(Product, AdminProduct)
admin.site.register(Category , AdminCategory)
admin.site.register(Order, AdminOrder )
admin.site.register(Brand,AdminBrand )
