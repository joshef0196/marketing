from django.contrib import admin
from .import models
from django.utils.html import format_html

class RegistrationAdmin(admin.ModelAdmin):
    list_display    = ['name','email','mobile','reg_date','status']
    search_fields   = ['name','email','mobile','reg_date','status']
    list_filter     = ['name','status']

admin.site.register(models.Registration,RegistrationAdmin)
