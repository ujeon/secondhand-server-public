from django.shortcuts import render

from .bungae_crawler import Bungae_crawler
from .daangn_crawler import daangn_crawler
from .hello_crawler import hello_crawler

from .models import Raw_data, Filtered_data, Average_price, Category
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
from multiprocessing import Pool
from django.db.models import Q
import json
import threading
from .filter_save import retrieve_raw_data
from .average_price_save import retrieve_filtered_data


# Create your views here.

# result page
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


# search page
def handle_search_price(request):
    request_body = json.loads(request.body)

    if request_body["brand"] and request_body["model"]:
        price_filtered_data = Filtered_data.objects.filter(
            price__range=[request_body["min_price"], request_body["max_price"]],
            brand=request_body["brand"],
            model=request_body["model"],
        )

    else:
        price_filtered_data = Filtered_data.objects.filter(
            price__range=[request_body["min_price"], request_body["max_price"]]
        )

    temp = []
    for data in price_filtered_data.values():
        average_price = Average_price.objects.filter(
            Q(brand=data["brand"]) | Q(model=data["model"])
        ).values()[0]

        data["average_price"] = average_price["average_price"]
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
    category_id = Category.objects.filter(category_name=category).values("id")[0]
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
    category_id = Category.objects.filter(category_name=category).values("id")[0]
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


def multi_crawl_save():
    bungae_func = Bungae_crawler("유모차")
    bungae_func.data_maker(100)
    daangn_crawler(10)
    hello_crawler(10)
    return


def save_hook():
    Raw_data.objects.all().delete()
    multi_crawl_save()
    retrieve_raw_data()
    retrieve_filtered_data()


def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t


def save_all_auto(request):
    save_hook()
    set_interval(save_hook, 86400)
    return HttpResponse(status=200)
