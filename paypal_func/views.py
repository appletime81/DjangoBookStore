from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from cart.views import get_member_data
from order.models import OrderList, Order
from django.db.models import Max, Sum
from paypal.standard.forms import PayPalPaymentsForm
from MyFinalHW import settings


# Create your views here.
@csrf_exempt
def cancel_func(request):
    message = '已完成付款'
    return render(request, 'payment_calcled.html', locals())


@csrf_exempt
# @login_required
def payment_func(request):
    current_user, verified = get_member_data(request)
    host = request.get_host()
    save_order_dict = {
        'user': current_user,
    }
    order = Order(**save_order_dict)
    order.save()
    max_id = Order.objects.filter().aggregate(Max('id'))['id__max']
    order_list_query = OrderList.objects.filter(user=current_user, paid=False)
    total_price = OrderList.objects.filter(user=current_user, paid=False).aggregate(Sum('price')).get('price__sum')
    order = Order(user=current_user)
    order_list_query.update(order_id=max_id)


    paypal_dict = {
        'business': settings.PAYPAL_REVEIVER_EMAIL,
        'amount': total_price,
        'item_name': f'訂單編號: {max_id}',
        'invoice:': f'invoice-{max_id}',
        'currency_code': 'TWD',
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return_url': f'http://{host}/done',
        'cancel_return': f'http://{host}/canceled',
    }
    paypal_form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment_test.html', locals())


@csrf_exempt
def done_func(request):
    message = '已完成付款'
    return render(request, 'payment_done.html', locals())
