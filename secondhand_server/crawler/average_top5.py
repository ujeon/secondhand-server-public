from django.http import HttpResponse, JsonResponse, HttpRequest
from .models import Average_price
import datetime
import json


def average_price_in_month(model):
    today = datetime.date.today()
    month_ago = today - datetime.timedelta(30)
    average_price_data = Average_price.objects.filter(
        date__range=[month_ago, today], model=model).values()

    total_trade_price = 0
    total_trade_quantity = 0

    for data in average_price_data:
        total_trade_price += (data["average_price"] * data["quantity"])
        total_trade_quantity += data["quantity"]

    return int(total_trade_price / total_trade_quantity)


def average_top5(request):
    model_dict = {}
    average_price_list = Average_price.objects.exclude(
        model="반려동물 유모차").values()
    for data in average_price_list:
        if model_dict.get(data["model"]):
            model_dict[data["model"]] += data["quantity"]
        else:
            model_dict[data["model"]] = data["quantity"]
    top_5_list = sorted(model_dict, key=model_dict.get, reverse=True)[:5]
    result_list = []
    for model in top_5_list:
        model_dictionary = {
            "model": model,
            "averge_price": average_price_in_month(model),
            "quantity": model_dict[model]
        }
        result_list.append(model_dictionary)

    return JsonResponse(result_list, safe=False)
