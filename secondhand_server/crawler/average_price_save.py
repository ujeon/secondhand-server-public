from django.http import HttpResponse
from .models import Filtered_data, Average_price
from .average_price_func import average_price_func


def input_fitered_data(data):
    try:
        new_data = Average_price(
            brand=data["brand"],
            model=data["model"],
            date=data["date"],
            average_price=data["average_price"],
            lowest_price=data["lowest_price"],
            highest_price=data["highest_price"],
            quantity=data["quantity"]
        )
        new_data.save()
        return HttpResponse(status=200)
    except Exception as ex:
        print("정상 작동중이니 당황하지 마세요", ex)
        return HttpResponse(status=500)


# DB에서 filtered data를 불러오는 함수
def retrieve_filtered_data():
    data_set_by_model = (
        Filtered_data.objects.exclude(model="etc")
        .values_list("model", flat=True).distinct()
    )
    data_set_by_date = (
        Filtered_data.objects.exclude(model="etc")
        .values_list("posted_at", flat=True).distinct()
    )
    data_set_by_average_model = (
        Average_price.objects.values_list("model", flat=True)
    )
    data_set_by_average_date = (
        Average_price.objects.values_list("date", flat=True)
    )
    for models in data_set_by_model:
        for date in data_set_by_date:
            if (models not in data_set_by_average_model) or (date not in data_set_by_average_date):
                filtered_data = Filtered_data.objects.filter(
                    model=models, posted_at=date)
                average_price_data = average_price_func(filtered_data)
                input_fitered_data(average_price_data)
    return
