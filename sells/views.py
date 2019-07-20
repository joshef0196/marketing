from django.shortcuts import render,redirect,HttpResponse
from . import models
from django.contrib import messages
from django.db.models import Sum
from django.db.models import F,Q

def salesman_dashboard(request):
    
    return render(request,'sells/salesman/index.html')

def admin_dashboard(request):
    
    return render(request,'sells/admin/index.html')

def registration(request):
    
    return render(request,'sells/admin/registration.html')

def Login(request):
    
    return render(request,'sells/page-login.html')

def Login1(request):
    
    return render(request,'sells/page-login.html')
