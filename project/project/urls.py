"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='index'),
    path('Registration/',views.Registration,name='Registration'),
    path('login/',views.login,name='login'), 
    path('logout/',views.logout,name='logout'),
    path('home/',views.home,name='home'),
    path('market/',views.market,name='market'),


           # Forgot Password URLS

    path('forgot/', views.forgot, name='forgot'),
    path('enteremail/', views.enteremail, name='enteremail'),
    path('reset/', views.reset, name='reset'),
        
    



           # Admin Dashboard URLS

    path('admindashboard/',views.admindashboard,name='admindashboard'),
    path('admindashboard/add_dep/',views.add_dep,name='add_dep'),
    path('admindashboard/show_dep/',views.show_dep,name='show_dep'),
    path('admindashboard/save_dep/',views.save_dep,name='save_dep'),
    path('admindashboard/add_emp/',views.add_emp,name='add_emp'),
    path('admindashboard/save_emp/',views.save_emp,name='save_emp'),
    path('admindashboard/show_emp/',views.show_emp,name='show_emp'),
    path('admindashboard/edit_dep/<int:id>/', views.edit_dep, name='edit_dep'),
    path('admindashboard/update_dep/<int:id>/', views.update_dep, name='update_dep'),
    path('admindashboard/delete_dep/<int:id>/', views.delete_dep, name='delete_dep'),
    path('admindashboard/edit_emp/<int:id>/', views.edit_emp, name='edit_emp'),
    path('admindashboard/update_emp/<int:id>/', views.update_emp, name='update_emp'),
    path('admindashboard/delete_emp/<int:id>/', views.delete_emp, name='delete_emp'),
    path('admindashboard/emp_all_query/',views.emp_all_query,name='emp_all_query'),
    path('admindashboard/emp_all_query/reply/<int:pk>/',views.reply,name='reply'),
    path('admindashboard/emp_all_query/a_reply/<int:pk>/',views.a_reply,name='a_reply'),
    path('admindashboard/add_item/',views.add_item,name='add_item'),
    path('admindashboard/show_item/',views.show_item,name='show_item'),



          # User Dashboard URLS

    path('userdashboard/',views.userdashboard,name='userdashboard'),


          # Employee Dashboard URLS
    path('empdashboard/',views.empdashboard,name='empdashboard'),
    path('empdashboard/profile/',views.profile,name='profile'),
    path('empdashboard/setting/',views.setting,name='setting'),
    path('empdashboard/query/',views.query,name='query'),
    path('empdashboard/querydata/',views.querydata,name='querydata'),
    path('empdashboard/allquery/',views.allquery,name='allquery'),
    path('empdashboard/pendingquery/',views.pendingquery,name='pendingquery'),
    path('empdashboard/donequery/',views.donequery,name='donequery'),
    path('empdashboard/edit_all_query/<int:pk>/',views.edit_all_query,name='edit_all_query'),
    path('empdashboard/updated_query/<int:pk>/', views.updated_query, name='updated_query'),
    path('empdashboard/emp_q_delete/<int:id>/', views.emp_q_delete, name='emp_q_delete'),
    path('empdashboard/allquery/search/', views.search, name='search'),
    



           # Payment URLS

    path('userdashboard/payment/<int:pk>/',views.payment,name='payment'),
    path('pay_amount/<int:pk>/',views.pay_amount,name='pay_amount'),
    path('pay_status/<int:pk>/',views.pay_status,name='pay_status'),


           # Cart URLS
           
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_page, name='cart_page'),
    path('remove-cart/<int:id>/', views.remove_cart, name='remove_cart'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
