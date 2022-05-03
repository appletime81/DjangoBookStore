"""BookStore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include, re_path
from cart.views import index, listing
from order.views import checkout, OrderView, OrderDeleteView
from ProductItroduction.views import ProductIntroduction
from ShoppingList.views import ShoppingListView
from paypal_func import views
from Profile.views import ProfileView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('listing/', listing),
    path('productinfo/<str:productname>', ProductIntroduction.as_view()),
    path('checkout/', checkout, name='checkout-url'),
    path('order/list', OrderView.as_view(), name='order-url'),
    path('order/list/<str:itemName>', OrderView.as_view(), name='order-url'),
    path('order/delete/<str:deleteItem>/<str:order_time>', OrderDeleteView.as_view()),
    path('shoppinglist/', ShoppingListView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('payment_test/', views.payment_func),
    path('accounts/', include('allauth.urls')),
    path('paypal/', include('paypal.standard.ipn.urls')),
    re_path(r'^payment/(\d+)/$', views.payment_func),
    path('done/', views.done_func),
    re_path(r'^canceled/$', views.cancel_func)
]
