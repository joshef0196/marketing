from sells import views
from django.urls import path

urlpatterns = [
    path('dashboard/',views.salesman_dashboard),
    path('admin-dashboard/',views.admin_dashboard),
    path('salesman-registration/',views.registration),
    path('',views.Login),
]
