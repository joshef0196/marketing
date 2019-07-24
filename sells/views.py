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
    if not request.session['usertype'] == "admin":
        return redirect('/')

    return render(request,'sells/admin/index.html')

def admin_product_add(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')

    product_cat = models.ProductCat.objects.all().order_by("category_name")
    context = {
        'product_cat': product_cat,       
    }
    if request.method=="POST":
        product_cat          = int(request.POST['product_cat'])
        product_name         = request.POST['product_name']
        brand_name           = request.POST['brand_name']
        product_model_number = request.POST['product_model_number']
        product_color        = request.POST['product_color']
        unit_price           = request.POST['unit_price']
        total_quantity       = request.POST['total_quantity']
        buy_price            = request.POST['buy_price']
        discount             = request.POST['discount']
        discription          = request.POST['discription']
        total_price          = round((int(total_quantity)*float(unit_price)),2)
        if models.Product.objects.create(
            category_name_id = product_cat, product_name = product_name, brand_name = brand_name, product_model_number = product_model_number,product_color = product_color,
            unit_price = unit_price, total_quantity = total_quantity, available_quantity = total_quantity, buy_price = buy_price,
            discount = discount, total_price = total_price, discription = discription):
            return redirect("/product-list/")
        else:
            return redirect("/product-add/") 
    return render(request,'sells/admin/add_product.html',context)

def product_list(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')

    product = models.Product.objects.filter(status = True).order_by("id")
    context = {
        'product': product,       
    }
    return render(request,'sells/admin/product_list.html',context)

def edit_product(request,id):
    if not request.session['usertype'] == "admin":
        return redirect('/')

    context={
        'edit_product': models.Product.objects.filter(id = id).first(),
        'product_cat': models.ProductCat.objects.filter(status = True),
    }
    if request.method=="POST":
        product_cat          = int(request.POST['product_cat'])
        product_name         = request.POST['product_name']
        brand_name           = request.POST['brand_name']
        product_model_number = request.POST['product_model_number']
        product_color        = request.POST['product_color']
        unit_price           = request.POST['unit_price']
        total_quantity       = request.POST['total_quantity']
        buy_price            = request.POST['buy_price']
        discount             = request.POST['discount']
        discription          = request.POST['discription']
        total_price          = round((int(total_quantity)*float(unit_price)),2)
        
        models.Product.objects.filter(id = id).update(category_name_id = product_cat, product_name = product_name, brand_name = brand_name, product_model_number = product_model_number,product_color = product_color,
            unit_price = unit_price, total_quantity = total_quantity, available_quantity = total_quantity, buy_price = buy_price,
            discount = discount, total_price = total_price, discription = discription)
        return redirect("/product-list/")

    return render(request,'sells/admin/edit_product.html',context)


def registration(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')

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
