from sells import views
from django.urls import path

urlpatterns = [
    path('',views.login),
    path('logout/',views.logout),
    path('change-password/',views.change_password),

    #.............. for salesman.................
    path('all-product-list/',views.sales_product_list),
    path('add-sales-product/',views.add_selling_product),
    path('category/product-load/',views.load_category_product),

    #.............. for admin....................
    path('admin-dashboard/',views.admin_dashboard),
    path('product-add/',views.admin_product_add),
    path('edit/<int:id>/',views.edit_product),
    path('product-list/',views.product_list),
    path('salesman-registration/',views.registration),

    #.................... Report.....................
    #....For Admin.......#
    path('daily-report/', views.daily_report),
    path('yearly-report/', views.yearly_report),
    path('monthly-report/', views.monthly_report),
    path('date-wise-report/', views.date_to_date_report),
    path('salesman-wise-report/', views.man_wise_report),
    #....For Saleman.......#
    path('my-daily-report/', views.salesman_daily_report),
    path('my-date-wise-report/', views.salesman_date_to_date_report),
    

]
