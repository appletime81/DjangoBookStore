from django.shortcuts import render
from allauth.account.admin import EmailAddress
from .models import Commodity
from django.core.paginator import Paginator


def index(request):
    if request.method == "GET":
        current_user, verified = get_member_data(request)
    return render(request, 'index.html', locals())


def listing(request):
    if request.method == "GET":
        current_user, verified = get_member_data(request)
        products = Commodity.objects.all()
        paginator = Paginator(products, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    return render(request, 'listing.html', locals())


# --------------------會員授權認證------------------
def get_member_data(request):
    try:
        current_user = request.user
        verified = EmailAddress.objects.filter(user=current_user).values()[0]
        verified = verified["verified"]
        # print(f'當前使用者: {request.user}')
        # print(f'當前使用者信箱認證: {verified}')
    except Exception:
        verified = False
    return current_user, verified
