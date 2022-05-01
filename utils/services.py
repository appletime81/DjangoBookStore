
class CalculateOrderListTotalPrice:
    @staticmethod
    def cal(not_paid_item_list):
        total_price = 0
        for item in not_paid_item_list:
            total_price += item.get('price')
        return total_price
