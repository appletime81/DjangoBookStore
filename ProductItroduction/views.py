from django.shortcuts import render, redirect
from django.views import View
from cart.views import get_member_data
from cart.models import Commodity
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from order.models import OrderList
from datetime import datetime


# Create your views here.
class ProductIntroduction(View):
    def get(self, request, **kwargs):
        current_user, verified = get_member_data(request)
        commodity = Commodity.objects.filter(itemName=kwargs.get('productname')).values()[0]
        print(commodity)
        return render(request, 'ProductInfo.html', locals())

    @method_decorator(login_required)
    def post(self, request, **kwargs):
        current_user, verified = get_member_data(request)
        commodity = Commodity.objects.filter(itemName=kwargs.get('productname')).values()[0]
        print('commodity:', commodity)
        current_user, verified = get_member_data(request)
        value_dict = request.POST.dict()
        qty = value_dict.get('qty_value')
        itemName = kwargs.get('productname')
        order_time = datetime.now()
        order_time_str = order_time.strftime('%Y-%m-%d %H:%M:%S')
        product = Commodity.objects.filter(itemName=itemName)
        product_info = product.values()[0]
        price = product_info.get('price')
        productname = kwargs.get('productname')
        alert_msg = None
        non_verified_msg = None

        try:
            if verified:
                qty = int(qty)
                if qty > 0:
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
                        oder_list = OrderList(**save_data_dict)
                        oder_list.save()
                    message_add_cart = '已放入購物車'
                else:
                    alert_msg = '請輸入正確數字'
            else:
                non_verified_msg = '請先至個人信箱驗證'
        except:
            alert_msg = '請輸入正確數字'
        return render(request, 'ProductInfo.html', locals())