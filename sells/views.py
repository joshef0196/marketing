from django.shortcuts import render,redirect,HttpResponse
from . import models
from django.contrib import messages
from django.db.models import Sum, F,Q
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from sells.utils import render_to_pdf

def salesman_dashboard(request):
    
    return render(request,'sells/salesman/index.html')

def admin_dashboard(request):
    if not request.session['user']:
        return redirect('/')

    return render(request,'sells/admin/index.html')

def admin_product_add(request):
    if not request.session['user']:
        return redirect('/')
    product_cat = models.ProductCat.objects.all()
    context = {
        'product_cat': product_cat,       
    }
    return render(request,'sells/admin/add_product.html',context)

def product_list(request):
    if not request.session['user']:
        return redirect('/')

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

def login(request):
    if request.method=="POST":
        username  = request.POST['username']
        password  = request.POST['password']
        user      = User.objects.filter(username=username).first()
        if user:
            pwd_valid = check_password(password, user.password)
            if pwd_valid:
                request.session['user'] = user.username
                request.session['usertype'] = 'admin'
                return redirect("/admin-dashboard/")
        else:
            user  = models.Registration.objects.filter(mobile = username, password = password)
            if user:
                request.session['user'] = user[0].name
                request.session['usertype'] = 'salesman'
                return redirect("/dashboard/")
    return render(request,'sells/page_login.html')
    
def logout(request):  
    request.session['user'] = False
    request.session['usertype'] = False
    return redirect('/')


def daily_report(request):
    
    pdf = render_to_pdf('sells/admin/daily_report.html')
    return HttpResponse(pdf, content_type='application/pdf')

def weekly_report(request):
    
    pdf = render_to_pdf('sells/admin/weekly_report.html')
    return HttpResponse(pdf, content_type='application/pdf')

def monthly_report(request):
    
    pdf = render_to_pdf('sells/admin/monthly_report.html')
    return HttpResponse(pdf, content_type='application/pdf') 
