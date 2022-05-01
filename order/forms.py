from django import forms
from .models import OrderList


class OrderListForm(forms.ModelForm):
    class Meta:
        model = OrderList
        fields = ['qty']

    def __init__(self, *args, **kwargs):
        super(OrderListForm, self).__init__(*args, **kwargs)
        self.fields['qty'].label = '數量'
