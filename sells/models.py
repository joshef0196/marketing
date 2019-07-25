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
    brand_name           = models.CharField(max_length=150, blank=True)
    product_model_number = models.CharField(max_length=100, blank=True)
    product_color        = models.CharField(max_length=50, blank=True)
    available_quantity   = models.IntegerField(default=1)
    total_quantity       = models.IntegerField(default=1)
    unit_price           = models.FloatField(default=0)
    total_price          = models.FloatField(default=0)
    buy_price            = models.FloatField(default=0)
    discount             = models.FloatField(default=0, blank=True)
    discription          = models.TextField(blank=True)
    status               = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name        ='Product'
        verbose_name_plural ='Products'

class SalesProduct(models.Model):
    salesman             = models.ForeignKey(Registration, on_delete=models.CASCADE)
    product              = models.ForeignKey(Product, on_delete=models.CASCADE)
    total_price          = models.FloatField(default=0)
    sale_quantity        = models.IntegerField(default=1)
    discount             = models.FloatField(default=0, blank=True)
    comment              = models.TextField(blank=True)
    sale_date            = models.DateTimeField(auto_now_add=True)
    status               = models.BooleanField(default=True)

    def __str__(self):
        return str(self.salesman)

    class Meta:
        verbose_name        ='Sales Product'
        verbose_name_plural ='Sales Products'
