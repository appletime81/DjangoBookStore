from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from order.models import OrderList, Order
from cart.views import get_member_data


def payment_notification(sender, **kwargs):

    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        order_id = ipn_obj.invoice.split('-')[-1]
        order_list = OrderList.objects.filter(id=order_id, paid=False)
        order_list.update(paid=True)
        order = Order.objects.filter(id=order_id)
        order.update(paid=True)

valid_ipn_received.connect(payment_notification)
