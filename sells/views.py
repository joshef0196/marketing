from django.shortcuts import render,redirect,HttpResponse
from . import models
from django.contrib import messages
from django.db.models import F,Q
from django.db.models import Sum
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from sells.utils import render_to_pdf
from django.http import HttpResponse, JsonResponse
import datetime
import hashlib, socket
from django.utils.dateparse import parse_date, parse_datetime

# .............For Admin.................
def admin_dashboard(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')

    today_sale       = models.SalesProduct.objects.filter(sale_date__date = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d")).aggregate(Sum('total_price'))['total_price__sum']
    today_pro_buy    = models.SalesProduct.objects.filter(sale_date__date = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d")).aggregate(Sum('product__buy_price'))['product__buy_price__sum']
    total_sale       = models.SalesProduct.objects.filter(status=True).aggregate(Sum('total_price'))['total_price__sum']
    data_list        = models.SalesProduct.objects.filter(sale_date__date = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d"), status = True)
    data_list        = models.SalesProduct.objects.raw('SELECT (select sum(pp.buy_price * s.sale_quantity) from sells_salesproduct s inner join sells_product pp on pp.id = s.product_id WHERE pp.id = sp.product_id and DATE(s.sale_date) = %s) as buy_price FROM sells_salesproduct sp inner join sells_product p on p.id = sp.product_id WHERE DATE(sp.sale_date) = %s group by sp.product_id', datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d"), datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d"))

    # today_buy_price = data_list.product[0].buy_price * data_list.sale_quantity
    # today_profit = 0
    # if today_buy_price :
    #     today_profit    = data_list.total_price - today_buy_price
    
    context={
        'today_sale': today_sale,
        'today_pro_buy': today_pro_buy,
        # 'today_profit': today_profit,
        'total_sale': total_sale,
    }
    return render(request,'sells/admin/index.html',context)

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

    product = models.Product.objects.filter(status = True).order_by("-id")
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

# .....Report..........#

def daily_report(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')
    daily_sell             = models.SalesProduct.objects.filter(sale_date__date = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d"))
    company                = models.Content.objects.filter(status = True).first()

    today_product_sales    = models.SalesProduct.objects.filter(sale_date__date = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d")).aggregate(Sum('sale_quantity'))['sale_quantity__sum']
    today_sale             = models.SalesProduct.objects.filter(sale_date__date = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d")).aggregate(Sum('total_price'))['total_price__sum']
    today_pro_buy          = models.SalesProduct.objects.filter(sale_date__date = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d")).aggregate(Sum('product__buy_price'))['product__buy_price__sum']
    today_discount_amount  = models.SalesProduct.objects.filter(sale_date__date = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d")).aggregate(Sum('discount'))['discount__sum']
    today_profit = 0
    if today_sale :
        today_profit = today_sale - today_pro_buy
    
    context={
        "daily_sell":daily_sell,
        "company":company,
        'today_product_sales': today_product_sales,
        'today_sale': today_sale,
        'today_discount_amount': today_discount_amount,
        'today_profit': today_profit,
    }
    pdf = render_to_pdf('sells/admin/daily_report.html',context)
    return HttpResponse(pdf, content_type='application/pdf')

def monthly_report(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')
    monthly_sell = models.SalesProduct.objects.filter(sale_date__month = datetime.datetime.now().month)
    company      = models.Content.objects.filter(status = True).first()

    today_product_sales    = models.SalesProduct.objects.filter(sale_date__month = datetime.datetime.now().month, status = True).aggregate(Sum('sale_quantity'))['sale_quantity__sum']
    today_sale             = models.SalesProduct.objects.filter(sale_date__month = datetime.datetime.now().month, status = True).aggregate(Sum('total_price'))['total_price__sum']
    today_pro_buy          = models.SalesProduct.objects.filter(sale_date__month = datetime.datetime.now().month, status = True).aggregate(Sum('product__buy_price'))['product__buy_price__sum']
    today_discount_amount  = models.SalesProduct.objects.filter(sale_date__month = datetime.datetime.now().month, status = True).aggregate(Sum('discount'))['discount__sum']
    today_profit = 0
    if today_sale :
        today_profit = today_sale - today_pro_buy
    
    context={
        "monthly_sell":monthly_sell,
        "company":company,
        'today_product_sales': today_product_sales,
        'today_sale': today_sale,
        'today_discount_amount': today_discount_amount,
        'today_profit': today_profit,
    }
    pdf = render_to_pdf('sells/admin/monthly_report.html',context)
    return HttpResponse(pdf, content_type='application/pdf') 

def yearly_report(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')
    yearly_sell = models.SalesProduct.objects.filter(sale_date__year = datetime.datetime.now().year, status = True)
    company     = models.Content.objects.filter(status = True).first()

    today_product_sales    = models.SalesProduct.objects.filter(sale_date__year = datetime.datetime.now().year, status = True).aggregate(Sum('sale_quantity'))['sale_quantity__sum']
    today_sale             = models.SalesProduct.objects.filter(sale_date__year = datetime.datetime.now().year, status = True).aggregate(Sum('total_price'))['total_price__sum']
    today_pro_buy          = models.SalesProduct.objects.filter(sale_date__year = datetime.datetime.now().year, status = True).aggregate(Sum('product__buy_price'))['product__buy_price__sum']
    today_discount_amount  = models.SalesProduct.objects.filter(sale_date__year = datetime.datetime.now().year, status = True).aggregate(Sum('discount'))['discount__sum']
    today_profit = 0
    if today_sale :
        today_profit = today_sale - today_pro_buy
    
    context={
        "yearly_sell":yearly_sell,
        "company":company,
        'today_product_sales': today_product_sales,
        'today_sale': today_sale,
        'today_discount_amount': today_discount_amount,
        'today_profit': today_profit,
    }
    pdf = render_to_pdf('sells/admin/yearly_report.html', context)
    return HttpResponse(pdf, content_type='application/pdf')

def date_to_date_report(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')
    if request.method == "POST":
        from_date = parse_date(request.POST['from_date'])
        to_date   = parse_date(request.POST['to_date'])

        date_to_date_sell      = models.SalesProduct.objects.filter(sale_date__date__gte = from_date, sale_date__date__lte = to_date, status=True )
        company                = models.Content.objects.filter(status = True).first()
        today_product_sales    = models.SalesProduct.objects.filter(sale_date__date__gte = from_date, sale_date__date__lte = to_date, status=True).aggregate(Sum('sale_quantity'))['sale_quantity__sum']
        today_sale             = models.SalesProduct.objects.filter(sale_date__date__gte = from_date, sale_date__date__lte = to_date, status=True).aggregate(Sum('total_price'))['total_price__sum']
        today_pro_buy          = models.SalesProduct.objects.filter(sale_date__date__gte = from_date, sale_date__date__lte = to_date, status=True).aggregate(Sum('product__buy_price'))['product__buy_price__sum']
        today_discount_amount  = models.SalesProduct.objects.filter(sale_date__date__gte = from_date, sale_date__date__lte = to_date, status=True).aggregate(Sum('discount'))['discount__sum']

        today_profit = 0
        if today_sale :
            today_profit = today_sale - today_pro_buy
        context = {
            'from_date':from_date,
            'to_date':to_date,
            "date_to_date_sell":date_to_date_sell,
            "company":company,
            'today_product_sales': today_product_sales,
            'today_sale': today_sale,
            'today_discount_amount': today_discount_amount,
            'today_profit': today_profit,
        }
        if date_to_date_sell:
            pdf = render_to_pdf('sells/admin/date_to_date_pdf.html', context)
            return HttpResponse(pdf, content_type='application/pdf')
        else:    
            return render(request,'sells/admin/date_to_date_report.html', context)
    return render(request,'sells/admin/date_to_date_report.html')

def summary_report(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')
        
    if request.method == "POST":
        from_date = parse_date(request.POST['from_date'])
        to_date   = parse_date(request.POST['to_date'])

        company                = models.Content.objects.filter(status = True).first()
        sale_summary_report    = models.SalesProduct.objects.raw('SELECT sp.id, sp.sale_date as sale_date, sum(sp.total_price) as total_price, sum(sp.sale_quantity) as sale_quantity, sum(sp.discount) as discount, sum(sp.total_buy) as total_buy FROM sells_salesproduct sp inner join sells_product p on p.id = sp.product_id WHERE DATE(sp.sale_date) between %s and %s and sp.status = true group by DATE(sp.sale_date)',[from_date ,to_date])
        
        if len(list(sale_summary_report)) > 0:
            context = {
                'from_date':from_date,
                'to_date':to_date,
                "company":company,
                'sale_summary_report': sale_summary_report,
                'sale_summary_count': len(list(sale_summary_report)),
            }
            pdf = render_to_pdf('sells/admin/sumarry_report_pdf.html', context)
            return HttpResponse(pdf, content_type='application/pdf')
        else:   
            context = {
                'from_date':from_date,
                'to_date':to_date,
                "company":company,
                'sale_summary_report': sale_summary_report,
                'sale_summary_count': len(list(sale_summary_report)),
            } 
            return render(request,'sells/admin/summary_report.html', context)
    return render(request,'sells/admin/summary_report.html')

def man_wise_report(request):
    if not request.session['usertype'] == "admin":
        return redirect('/')
    salesman_list = models.Registration.objects.filter(status = True).all()
    if request.method == "POST":
        salesman_id  = int(request.POST['salesman'])
        from_date    = parse_date(request.POST['from_date'])
        to_date      = parse_date(request.POST['to_date'])

        date_to_date_sell      = models.SalesProduct.objects.filter(sale_date__date__gte = from_date, sale_date__date__lte = to_date,salesman_id = salesman_id, status=True )
        company                = models.Content.objects.filter(status = True).first()

        today_product_sales    = models.SalesProduct.objects.filter(sale_date__date__gte = from_date, sale_date__date__lte = to_date,salesman_id = salesman_id, status=True ).aggregate(Sum('sale_quantity'))['sale_quantity__sum']
        today_sale             = models.SalesProduct.objects.filter(sale_date__date__gte = from_date, sale_date__date__lte = to_date,salesman_id = salesman_id, status=True ).aggregate(Sum('total_price'))['total_price__sum']
        today_pro_buy          = models.SalesProduct.objects.filter(sale_date__date__gte = from_date, sale_date__date__lte = to_date,salesman_id = salesman_id, status=True ).aggregate(Sum('product__buy_price'))['product__buy_price__sum']
        today_discount_amount  = models.SalesProduct.objects.filter(sale_date__date__gte = from_date, sale_date__date__lte = to_date,salesman_id = salesman_id, status=True ).aggregate(Sum('discount'))['discount__sum']
        today_profit = 0
        if today_sale :
            today_profit = today_sale - today_pro_buy
    
        context = {
            'from_date':from_date,
            'to_date':to_date,
            'date_to_date_sell':date_to_date_sell,
            'company':company,
            'salesman_id':salesman_id,
            'today_product_sales': today_product_sales,
            'today_sale': today_sale,
            'today_discount_amount': today_discount_amount,
            'today_profit': today_profit,
        }
        if date_to_date_sell:      
            pdf = render_to_pdf('sells/admin/man_wise_report_pdf.html',context)
            return HttpResponse(pdf, content_type='application/pdf')
        else:
            context = {
                'from_date':from_date,
                'to_date':to_date,
                'date_to_date_sell':date_to_date_sell,
                'salesman_list':salesman_list,
                'salesman_id':salesman_id,
            }
        return render(request,'sells/admin/man_wise_report.html',context)
    return render(request,'sells/admin/man_wise_report.html',{"salesman_list" : salesman_list})

# .................End admin....................

# .................For salesman....................
def dashboard(request):
    if not request.session['usertype'] == "salesman":
        return redirect('/')
    today_sale          = models.SalesProduct.objects.filter( sale_date__date = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d"), salesman = request.session['salesman_id'] , status=True ).aggregate(Sum('total_price'))['total_price__sum']
    total_sale          = models.SalesProduct.objects.filter( salesman = request.session['salesman_id'] , status=True ).aggregate(Sum('total_price'))['total_price__sum']
    today_sale_product  = models.SalesProduct.objects.filter( sale_date__date = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d"), salesman = request.session['salesman_id'] , status=True ).aggregate(Sum('sale_quantity'))['sale_quantity__sum']
    total_sale_product  = models.SalesProduct.objects.filter( salesman = request.session['salesman_id'] , status=True ).aggregate(Sum('sale_quantity'))['sale_quantity__sum']
    context = {
        'today_sale': today_sale,       
        'total_sale': total_sale,       
        'today_sale_product': today_sale_product,       
        'total_sale_product': total_sale_product,       
    }
    return render(request,'sells/salesman/index.html',context)

def sales_product_list(request):
    if not request.session['usertype'] == "salesman":
        return redirect('/')
    product = models.SalesProduct.objects.filter(salesman_id = int(request.session['salesman_id']), status = True).order_by("-id")
    context = {
        'product': product,       
    }
    if request.method == "POST":
        product = request.POST['searchtxt']
        product_list = models.Product.objects.filter(Q(category_name__category_name__icontains = product)|Q(product_name__icontains = product))
        return render(request, 'sells/salesman/product_list.html',{'product_list' : product_list})

    return render(request,'sells/salesman/product_list.html',context)

def load_category_product(request):
    product_list = models.Product.objects.filter(category_name_id = int(request.GET.get('category_id')),available_quantity__gt = 0).order_by("product_name")

    return render(request, 'sells/salesman/load_product.html',{'product_list':product_list})

def add_selling_product(request):
    if not request.session['usertype'] == "salesman":
        return redirect('/')

    if request.method=="POST":
        product_id           = int(request.POST['product_name'])
        sell_quantity        = request.POST['sell_quantity']
        given_discount       = request.POST['given_discount']
        total_price          = request.POST['total_price']
        comment              = request.POST['comment']
        if not given_discount: given_discount = 0   
        product = models.Product.objects.filter(id = product_id, status = True)
        if product and product[0].available_quantity > 0:
            models.SalesProduct.objects.create(
                salesman_id = int(request.session['salesman_id']),product_id = product_id, sale_quantity = sell_quantity,
                discount = given_discount, total_price = total_price, total_buy = product[0].buy_price * float(sell_quantity),  comment = comment)
            product.update(available_quantity = F('available_quantity') - sell_quantity)
            messages.success(request,"Product successfully added")
        else:
            messages.warning(request,'Product not available')    
        return redirect("/add-sales-product/")    

    if request.is_ajax():
        product = models.Product.objects.values().filter(id = int(request.GET.get('product_id')), status = True, available_quantity__gt = 0).first()
        if not product: product = "not_found"
        return JsonResponse(product, safe = False, content_type='application/json; charset=utf8')

    product_list = models.ProductCat.objects.all().order_by("category_name")
    context = {
        'product_list': product_list,       
    }
    return render(request,'sells/salesman/add_product.html',context)

# .....Report..........#
def salesman_daily_report(request):
    if not request.session['usertype'] == "salesman":
        return redirect('/')

    daily_sell = models.SalesProduct.objects.filter(sale_date__date = datetime.datetime.strftime(datetime.datetime.now().date(),"%Y-%m-%d"), salesman = request.session['salesman_id'] , status=True )
    company = models.Content.objects.filter(status = True).first()
    pdf = render_to_pdf('sells/salesman/sales_daily_report.html', {"daily_sell":daily_sell, "company":company})
    return HttpResponse(pdf, content_type='application/pdf')

def salesman_date_to_date_report(request):
    if not request.session['usertype'] == "salesman":
        return redirect('/')
    
    if request.method == "POST":
        from_date = parse_date(request.POST['from_date'])
        to_date   = parse_date(request.POST['to_date'])
        date_to_date_sell = models.SalesProduct.objects.filter(sale_date__date__gte = from_date, sale_date__date__lte = to_date, salesman = request.session['salesman_id'], status=True  )
        company = models.Content.objects.filter(status = True).first()
        context = {
            'from_date':from_date,
            'to_date':to_date,
            "date_to_date_sell":date_to_date_sell,
            "company":company
        }
        if date_to_date_sell:
            pdf = render_to_pdf('sells/salesman/salesman_date_to_date_pdf.html', context)
            return HttpResponse(pdf, content_type='application/pdf')
        else:    
            return render(request,'sells/salesman/date_to_date_report.html', context)
    return render(request,'sells/salesman/date_to_date_report.html')

def salesman_summary_report(request):
    if not request.session['usertype'] == "salesman":
        return redirect('/')
        
    if request.method == "POST":
        from_date = parse_date(request.POST['from_date'])
        to_date   = parse_date(request.POST['to_date'])

        company                = models.Content.objects.filter(status = True).first()
        sale_summary_report    = models.SalesProduct.objects.raw('SELECT sp.id, sp.sale_date as sale_date, sum(sp.total_price) as total_price, sum(sp.sale_quantity) as sale_quantity, sum(sp.discount) as discount FROM sells_salesproduct sp inner join sells_product p on p.id = sp.product_id WHERE sp.salesman_id = %s and DATE(sp.sale_date) between %s and %s and sp.status = true group by DATE(sp.sale_date)',[int(request.session['salesman_id']),from_date ,to_date])
        
        if len(list(sale_summary_report)) > 0:
            context = {
                'from_date':from_date,
                'to_date':to_date,
                "company":company,
                'sale_summary_report': sale_summary_report,
                'sale_summary_count': len(list(sale_summary_report)),
            }
            pdf = render_to_pdf('sells/salesman/sumarry_report_pdf.html', context)
            return HttpResponse(pdf, content_type='application/pdf')
        else: 
            context = {
                'from_date':from_date,
                'to_date':to_date,
                "company":company,
                'sale_summary_report': sale_summary_report,
                'sale_summary_count': len(list(sale_summary_report)),
            }   
            return render(request,'sells/salesman/summary_report.html', context)
    return render(request,'sells/salesman/summary_report.html')


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
            new_md5_obj     = hashlib.md5(mobile.encode())
            new_enc_pass    = new_md5_obj.hexdigest()
            models.Registration.objects.create(name = name, email = email, mobile = mobile, password = new_enc_pass, address = address)
            messages.success(request,"Success!")
            return redirect('/salesman-registration/') 
        else:
            messages.warning(request,"Mobile number is already exits!")    
        
    return render(request,'sells/admin/registration.html')

def login(request):
    company = models.Content.objects.filter(status = True).first()
    context ={
        'company':company
    }
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
            new_md5_obj = hashlib.md5(password.encode())
            enc_pass    = new_md5_obj.hexdigest()
            user  = models.Registration.objects.filter(mobile = username, password = enc_pass)
            if user:
                request.session['user'] = user[0].name
                request.session['salesman_id'] = user[0].id
                request.session['usertype'] = 'salesman'
                return redirect("/dashboard/")
    return render(request,'sells/page_login.html',context)
    
def logout(request):  
    request.session['user'] = False
    request.session['usertype'] = False
    return redirect('/')

def change_password(request):
    company = models.Content.objects.filter(status = True).first()
    context ={
        'company':company
    }
    if request.method == "POST":
        current_pass = request.POST['current_pass']
        new_pass     = request.POST['new_pass']

        new_md5_obj = hashlib.md5(current_pass.encode())
        new_enc_pass = new_md5_obj.hexdigest()
        chk_user     = models.Registration.objects.filter(id = request.session['salesman_id'], password = new_enc_pass)
        if chk_user:
            new_md5_obj = hashlib.md5(new_pass.encode())
            new_enc_pass = new_md5_obj.hexdigest()
            models.Registration.objects.filter(id = request.session['salesman_id']).update(password = new_enc_pass)
            messages.success(request,'Your password has been changed.')
            return redirect("/change-password/")
        else:
            messages.warning(request,'Invalid current Password')

    return render(request,'sells/change_password.html',context)
