from django.http import HttpResponse, JsonResponse, HttpRequest
from .models import Average_price
import datetime
import json


def average_price_monthly(request):
    today = datetime.date.today()
    month_ago = today - datetime.timedelta(30)
    loaded_model = json.loads(request.body)["model"]
    average_price_data = Average_price.objects.filter(
        date__range=[month_ago, today], model=loaded_model).order_by("date").values()

    total_trade_price = 0
    total_trade_quantity = 0
    highest_price = 0
    lowest_price = average_price_data.first()["lowest_price"]
    daily = []

    for data in average_price_data:
        total_trade_price += (data["average_price"] * data["quantity"])
        total_trade_quantity += data["quantity"]
        if data["highest_price"] > highest_price:
            highest_price = data["highest_price"]
        if data["lowest_price"] < lowest_price:
            lowest_price = data["lowest_price"]
        daily.append(data)

    average_price_by_month = {
        "average_price": int(total_trade_price / total_trade_quantity),
        "lowest_price": lowest_price,
        "highest_price": highest_price,
        "daily": daily
    }

    return JsonResponse(average_price_by_month)
