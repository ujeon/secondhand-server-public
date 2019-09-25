from django.shortcuts import render

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

