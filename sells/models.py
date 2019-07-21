from django.db import models
from ckeditor.fields import RichTextField
from django.utils import timezone

class Registration(models.Model):
    name               = models.CharField(max_length=50)
    email              = models.EmailField(max_length=80,blank=True)
    mobile             = models.CharField(max_length=16,blank=True,unique=True)
    password           = models.CharField(max_length=100)
    address            = models.TextField(blank=True)
    reg_date           = models.DateField(auto_now_add=True)
    status             = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name        ='Registration'
        verbose_name_plural ='Registrations'

class ProductCat(models.Model):
    category_name      = models.CharField(max_length=100)
    status             = models.BooleanField(default=True)

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name        ='Product Category'
        verbose_name_plural ='Product Categories'

class Product(models.Model):
    category_name        = models.ForeignKey(ProductCat, on_delete=models.CASCADE)
    product_name         = models.CharField(max_length=100)
    brand_name           = models.CharField(max_length=150)
    product_model_number = models.CharField(max_length=100)
    product_color        = models.CharField(max_length=50, blank=True)
    quantity             = models.IntegerField(default=1)
    per_product_price    = models.FloatField(default=0)
    total_price          = models.FloatField(default=0)
    discount             = models.FloatField(default=0, blank=True)
    product_place        = models.CharField(max_length=150, blank=True)
    status               = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name        ='Product'
        verbose_name_plural ='Products'