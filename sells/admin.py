from django.contrib import admin
from .import models
from django.utils.html import format_html

class RegistrationAdmin(admin.ModelAdmin):
    list_display    = ['name','email','mobile','reg_date','status']
    search_fields   = ['name','email','mobile','reg_date','status']
    list_filter     = ['name','status']

class ProductCatAdmin(admin.ModelAdmin):
    list_display    = ['category_name','status']
    search_fields   = ['category_name','status']
    list_filter     = ['category_name','status']

class ProductAdmin(admin.ModelAdmin):
    list_display    = ['category_name','product_name','brand_name','quantity','product_color','product_model_number','per_product_price','total_price','status']
    search_fields   = ['category_name','product_name','status']
    list_filter     = ['category_name','product_name','status']

admin.site.register(models.Registration,RegistrationAdmin)
admin.site.register(models.ProductCat,ProductCatAdmin)
admin.site.register(models.Product,ProductAdmin)
