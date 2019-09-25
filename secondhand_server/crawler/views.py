from django.shortcuts import render
from django.http import HttpResponse

from .models import Raw_data
from .bungae_crawler import Bungae_crawler
from .daangn_crawler import daangn_crawler
from .hello_crawler import hello_crawler

from .models import Filtered_data, Average_price
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

def input_bungae_data(request):
    # REVIEW: 데이터를 크롤링 하고 DB에 저장합니다. 실패하면 except로 넘어갑니다.
    try:
        # REVIEW: 번개장터 데이터 크롤링
        bungae_crawler = Bungae_crawler("유모차")
        bungae_data = bungae_crawler.data_maker()

        # REVIEW: 헬로마켓 데이터 크롤링
        hello_data = hello_crawler()

        # REVIEW: 당근마켓 데이터 크롤링
        daangn_data = daangn_crawler()

        # REVIEW: 모든 데이터를 리스트에 저장합니다.
        all_data = [*bungae_data, *hello_data, *daangn_data]

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
    except:
        return HttpResponse(status=500)


