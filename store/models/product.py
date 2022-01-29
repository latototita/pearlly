from django.db import models
from .category import Category
from .brand import Brand


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=200, default='' , null=True , blank=True)
    image = models.ImageField(upload_to='uploads/products/')

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in =ids)


    @staticmethod
    def get_product_by_id(id):
        return Product.objects.filter(id__in =id)







    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        if category_id:
            return Product.objects.filter(category = category_id)
        else:
            return Product.get_all_products();


    @staticmethod
    def get_all_products_by_brandid(brand_id):
        if brand_id:
            return Product.objects.filter(brand = brand_id)
        else:
            return Product.get_all_products();


    @staticmethod
    def get_all_product():
        return Product.objects.filter(order__isnull=False).distinct()

    def __str__(self):
    
        return self.name
