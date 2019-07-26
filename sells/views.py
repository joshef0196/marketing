from django.shortcuts import render,redirect,HttpResponse
from . import models
from django.contrib import messages
from django.db.models import Sum, F,Q
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from sells.utils import render_to_pdf
from django.http import HttpResponse, JsonResponse
import datetime
from django.utils.dateparse import parse_date, parse_datetime
# .............For Admin.................
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
# .................End admin....................

# .................For salesman....................
def sales_product_list(request):
    if not request.session['usertype'] == "salesman":
        return redirect('/')
    product = models.Product.objects.filter(status = True).order_by("id")
    context = {
        'product': product,       
    }
    if request.method == "POST":
        product = request.POST['searchtxt']
        product_list = models.Product.objects.filter(Q(category_name__category_name__icontains = product)|Q(product_name__icontains = product))
        return render(request, 'sells/salesman/product_list.html',{'product_list' : product_list})

    return render(request,'sells/salesman/product_list.html',context)

def load_category_product(request):
    product_list = models.Product.objects.filter(category_name_id = int(request.GET.get('category_id'))).order_by("product_name")

    return render(request, 'sells/salesman/load_product.html',{'product_list':product_list})

def add_selling_product(request):
    if not request.session['usertype'] == "salesman":
        return redirect('/')
    if request.method=="POST":
        product_id          = int(request.POST['product_name'])
        sell_quantity        = request.POST['sell_quantity']
        given_discount       = request.POST['given_discount']
        total_price          = request.POST['total_price']
        comment              = request.POST['comment']
        if given_discount not in request.POST: 
            given_discount = 0
            
        if models.SalesProduct.objects.create(
            salesman_id = int(request.session['usertype'] == "salesman"),product_id = product_id, sale_quantity = sell_quantity,
            discount = given_discount, total_price = total_price, comment = comment):
            models.Product.objects.filter(id = product_id).update(available_quantity = F('available_quantity') - sell_quantity)
            messages.success(request,"Success!") 
        else:
            messages.warning(request,"Mobile number is already exits!")

    if request.is_ajax():
        product = models.Product.objects.values().filter(id = int(request.GET.get('product_id'))).first()
        return JsonResponse(product, safe = False, content_type='application/json; charset=utf8')

    product_list = models.ProductCat.objects.all().order_by("category_name")
    context = {
        'product_list': product_list,       
    }
    return render(request,'sells/salesman/add_product.html',context)

# .................End salesman....................

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
                request.session['salesman_id'] = user[0].id
                request.session['usertype'] = 'salesman'
                return redirect("/all-product-list/")
    return render(request,'sells/page_login.html')
    
def logout(request):  
    request.session['user'] = False
    request.session['usertype'] = False
    return redirect('/')


def daily_report(request):
    daily_sell = models.SalesProduct.objects.filter(sale_date__date__gte = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d"), sale_date__date__lte = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d"))
    pdf = render_to_pdf('sells/admin/daily_report.html', {"daily_sell":daily_sell})
    return HttpResponse(pdf, content_type='application/pdf')

def weekly_report(request):
    
    pdf = render_to_pdf('sells/admin/weekly_report.html')
    return HttpResponse(pdf, content_type='application/pdf')

def monthly_report(request):
    
    pdf = render_to_pdf('sells/admin/monthly_report.html')
    return HttpResponse(pdf, content_type='application/pdf') 
