from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from allauth.account.admin import EmailAddress
from cart.views import get_member_data


class ProfileView(View):
    @method_decorator(login_required)
    def get(self, request, **kwargs):
        current_user, verified = get_member_data(request)
        current_user = request.user
        user_email = EmailAddress.objects.filter(user=current_user).values()[0]
        return render(request, 'profile_setting.html', locals())
