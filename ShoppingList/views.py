from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from cart.views import get_member_data
from order.services import OrderService
from utils.services import CalculateOrderListTotalPrice
from pprint import pprint


class ShoppingListView(View):
    @method_decorator(login_required)
    def get(self, request, **kwargs):
        # 抓取會員權限
        current_user, verified = get_member_data(request)

        # 抓取所有訂單
        not_paid_order_list = OrderService.get_user_all_order_list(current_user, False)  # 抓取所有未結帳訂單
        paid_order_list = OrderService.get_user_all_order_list(current_user, True)  # 抓取所有已結帳訂單
        pprint(not_paid_order_list)

        # 計算總金額
        total_price_not_paid = CalculateOrderListTotalPrice.cal(not_paid_order_list)  # 計算未結帳訂單總金額
        total_price_paid = CalculateOrderListTotalPrice.cal(paid_order_list)  # 計算已結帳訂單總金額

        return render(request, 'shopping_list.html', locals())
