from django.shortcuts import render,redirect,HttpResponse
from . import models
from django.contrib import messages
from django.db.models import Sum
from django.db.models import F,Q

def salesman_dashboard(request):
    
    return render(request,'sells/salesman/index.html')

def admin_dashboard(request):
    
    return render(request,'sells/admin/index.html')

def admin_product_add(request):
    
    return render(request,'sells/admin/add_product.html')

def product_list(request):
    
    return render(request,'sells/admin/product_list.html')

def registration(request):
    if request.method=="POST":
        name          = request.POST['name']
        email         = request.POST['email']
        mobile        = request.POST['mobile']
        address       = request.POST['address']

        chk_user = models.Registration.objects.filter(mobile = mobile)
        if not chk_user:
            models.Registration.objects.create(name = name, email = email, mobile = mobile, password = mobile, address = address)
            messages.success(request,"Success!") 
        else:
            messages.warning(request,"Mobile number is already exits!")    
        
    return render(request,'sells/admin/registration.html')

def Login(request):
    
    return render(request,'sells/page-login.html')
    