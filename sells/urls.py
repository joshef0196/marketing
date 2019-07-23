from sells import views
from django.urls import path

urlpatterns = [
    path('',views.login),

    #.............. for salesman.................
    path('dashboard/',views.salesman_dashboard),

    #.............. for admin....................
    path('admin-dashboard/',views.admin_dashboard),
    path('product-add/',views.admin_product_add),
    path('product-list/',views.product_list),
    path('salesman-registration/',views.registration),

    #.................... Report.....................
    path('daily-report/', views.daily_report),
    path('weekly-report/', views.weekly_report),
    path('monthly-report/', views.monthly_report),

]
