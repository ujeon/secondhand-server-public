from django.shortcuts import render

from .models import Raw_data
from .bungae_crawler import Bungae_crawler
from .daangn_crawler import daangn_crawler
from .hello_crawler import hello_crawler

from .models import Filtered_data, Average_price, Category
from django.http import HttpResponse
from django.http import JsonResponse
from django.core import serializers
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


def input_bungae_data(request):
    # REVIEW: 데이터를 크롤링 하고 DB에 저장합니다. 실패하면 except로 넘어갑니다.
    try:
        # REVIEW: 번개장터 데이터 크롤링
        # bungae_crawler = Bungae_crawler("유모차")
        # bungae_data = bungae_crawler.data_maker(300)

        # REVIEW: 헬로마켓 데이터 크롤링
        hello_data = hello_crawler(10)

        # REVIEW: 당근마켓 데이터 크롤링
        # daangn_data = daangn_crawler(100)

        # REVIEW: 모든 데이터를 리스트에 저장합니다.
        all_data = [*hello_data]
# *bungae_data, *daangn_data
        for data in all_data:
            new_data = Raw_data(
                title=data["title"],
                content=data["content"],
                price=data["price"],
                url=data["url"],
                img_url=data["img_url"],
                market=data["market"],
                posted_at=data["posted_at"],
                is_sold=data["is_sold"],
                category_id=data["category_id"],
                location=data["location"],
            )
            new_data.save()
        return HttpResponse(status=200)
        # TOFIX: 어떤 에러인지 확인이 어렵습니다..!
    except Exception as err:
        print(err)
        pass
        return HttpResponse(status=500)


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
