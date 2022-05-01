from .models import OrderList
from pprint import pprint


class OrderService:
    @staticmethod
    def get_user_all_order_list(username, paid):
        all_order_list = list(OrderList.objects.filter(user=username, paid=paid).values())
        return all_order_list

