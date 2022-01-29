from django.db import  models

class Brand(models.Model):
    name = models.CharField(max_length=20)

    @staticmethod
    def get_all_brand():
        return Brand.objects.filter(product__isnull=False).distinct()


    def __str__(self):
        return self.name
