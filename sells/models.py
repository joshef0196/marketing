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
