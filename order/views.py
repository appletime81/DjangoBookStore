from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator

from cart.views import get_member_data
from .services import OrderService
from .forms import OrderListForm

# model
from cart.models import Commodity
from order.models import OrderList

from datetime import datetime
from utils.services import CalculateOrderListTotalPrice


# Create your views here.
@login_required
def checkout(request):
    if request.method == "GET":
        print('i am here..............')
        current_user, verified = get_member_data(request)
        previous_link = request.META.get('HTTP_REFERER')
        if 'listing' not in previous_link:
            previous_link = 'http://127.0.0.1:8000/listing'
        print('前一頁:', request.META.get('HTTP_REFERER'))
    return render(request, 'checkout.html', locals())


class OrderView(View):
    @method_decorator(login_required)
    def get(self, request, **kwargs):
        # 抓取點擊購物車後的商品資訊並顯示在表單上
        product = Commodity.objects.filter(itemName=kwargs.get('itemName'))
        print('product:', product)
        if product.exists():
            product_info = product.values()[0]

        order_time = datetime.now()
        order_time_str = order_time.strftime('%Y-%m-%d %H:%M:%S')
        order_list_form = OrderListForm()
        current_user, verified = get_member_data(request)

        # 抓取上一頁url
        previous_link = request.META.get('HTTP_REFERER')
        if 'listing' not in previous_link:
            previous_link = 'http://127.0.0.1:8000/listing'

        # 顯示客戶的所有訂單明細，並顯示是否已結帳
        all_order_list = OrderService.get_user_all_order_list(current_user, False)
        print('all_order_list:',all_order_list)
        total_price_not_paid = CalculateOrderListTotalPrice.cal(all_order_list)
        print('total_price_not_paid:', total_price_not_paid)

        return render(request, 'order.html', locals())

    @method_decorator(login_required)
    def post(self, request, itemName, *args, **kwargs):
        current_user, verified = get_member_data(request)
        product_info = Commodity.objects.filter(itemName=itemName).values()[0]  # 取得商品資訊
        order_time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 訂購時間
        order_list_form = OrderListForm()
        all_order_list = OrderService.get_user_all_order_list(current_user, False)  # 取得所有未付款訂單

        message_add_cart = None

        order_list_form = OrderListForm(request.POST)
        if order_list_form.is_valid():
            qty = order_list_form.cleaned_data.get('qty')
            if qty != 0 and qty > 0:
                price = product_info.get('price')
                order_list = OrderList.objects.filter(user=current_user, product_item=itemName, paid=False)
                if order_list.exists():
                    old_qty = list(order_list.values())[0].get('qty')
                    order_list.update(qty=qty + old_qty, order_time=order_time_str, price=(qty + old_qty) * price)
                else:
                    save_data_dict = {
                        'user': current_user,
                        'product_item': itemName,
                        'qty': qty,
                        'order_time': order_time_str,
                        'price': qty * price
                    }
                    order_list = OrderList(**save_data_dict)
                    order_list.save()
                message_add_cart = "已放入購物車"
            else:
                message = "請輸入商品數量"

            all_order_list = OrderService.get_user_all_order_list(current_user, False)
            total_price_not_paid = CalculateOrderListTotalPrice.cal(all_order_list)
            return render(request, 'order.html', locals())


class OrderDeleteView(View):
    @method_decorator(login_required)
    def get(self, request, deleteItem, order_time):
        current_user, verified = get_member_data(request)
        previous_link = request.META.get('HTTP_REFERER')
        delete_item = OrderList.objects.filter(
            user=current_user,
            product_item=deleteItem,
            order_time=order_time
        )
        delete_item.delete()
        return redirect(previous_link)
