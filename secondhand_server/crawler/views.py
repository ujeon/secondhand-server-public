from django.shortcuts import render

from .models import Raw_data
from .bungae_crawler import Bungae_crawler
from .daangn_crawler import daangn_crawler
from .hello_crawler import hello_crawler

from .models import Filtered_data, Average_price, Category
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from multiprocessing import Process
import json


# Create your views here.


def handle_each_model_info(request, brand, model):
    average_price = Average_price.objects.filter(brand=brand, model=model)
    filtered_data = Filtered_data.objects.filter(brand=brand, model=model)
    result = {}

    for data in average_price.values():
        result["average_price"] = data

    temp = []
    for data in filtered_data.values():
        temp.append(data)

    result["filtered_data"] = temp

    response = JsonResponse(result)

    return HttpResponse(response)


def handle_search_price(request):
    request_body = json.loads(request.body)

    if request_body["brand"] and request_body["model"]:
        price_filtered_data = Filtered_data.objects.filter(
            price__range=[request_body["min_price"],
                          request_body["max_price"]],
            brand=request_body["brand"],
            model=request_body["model"],
        )

    else:
        price_filtered_data = Filtered_data.objects.filter(
            price__range=[request_body["min_price"], request_body["max_price"]]
        )

    average_price = Average_price.objects.all()

    temp = []
    for data in price_filtered_data.values():
        for average_data in average_price.values():
            if (
                data["brand"] == average_data["brand"]
                and data["model"] == average_data["model"]
            ):
                data["average_price"] = average_data["average_price"]
                temp.append(data)

    response = JsonResponse(temp, safe=False)

    return HttpResponse(response)


# GET 요청
def search_route_brand_model(request):
    filtered_data = (
        Filtered_data.objects.all()
        .values("brand", "model")
        .order_by("brand", "model")
        .distinct()
    )
    result = []
    for data in filtered_data:
        result.append(data)

    response = JsonResponse(result, safe=False)

    return HttpResponse(response)


def get_categories(request):
    category_data = Category.objects.all().values()

    result = []
    for data in category_data:
        result.append(data)

    response = JsonResponse(result, safe=False)

    return HttpResponse(response)


def get_brands(request, category):
    category_id = Category.objects.filter(
        category_name=category).values("id")[0]
    filtered_data = (
        Filtered_data.objects.filter(category=category_id["id"])
        .values("brand")
        .order_by("brand")
        .distinct()
    )
    result = []
    for data in filtered_data:
        result.append(data)

    response = JsonResponse(result, safe=False)

    return HttpResponse(response)


def get_models(request, category, brand):
    category_id = Category.objects.filter(
        category_name=category).values("id")[0]
    filtered_data = (
        Filtered_data.objects.filter(category=category_id["id"], brand=brand)
        .values("model")
        .order_by("model")
        .distinct()
    )
    result = []
    for data in filtered_data:
        result.append(data)

    response = JsonResponse(result, safe=False)

    return HttpResponse(response)


def multi_crawl_save(request):
    try:
        # bungae_func = Bungae_crawler("유모차")
        hello_process = Process(target=hello_crawler(1))
        # daangn_process = Process(target=daangn_crawler())
        # bungae_process = Process(target=bungae_func())
        hello_process.start()
        # daangn_process.start()
        # bungae_process.start()
        return HttpResponse(status=200)
    except Exception as err:
        print(err)
        return HttpResponse(status=500)
