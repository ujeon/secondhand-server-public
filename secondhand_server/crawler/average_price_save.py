from django.http import HttpResponse
from .models import Raw_data, Filtered_data, Average_price
from .average_price_func import average_price_func


def input_fitered_data(all_data):
    # REVIEW: 데이터를 크롤링 하고 DB에 저장합니다. 실패하면 except로 넘어갑니다.
    try:
        for data in all_data:
            new_data = Average_price(
                brand=data["brand"]
                model=data["model"]
                date=data["date"]
                average_price=data["average_price"]
                lowest_price=data["lowest_price"]
                highest_price=data["highest_price"]
                quantity=data["quantity"]
            )
            new_data.save()
        return HttpResponse(status=200)
        # TOFIX: 어떤 에러인지 확인이 아래 코드로 가능합니다
    except Exception as ex:
        print("이것이 에러다!", ex)
        return HttpResponse(status=500)


# DB에서 filtered data를 불러오는 함수
def retrieve_filtered_data(request):
    data_set_by_model = (
        Filtered_data.objects.exclude(model="etc")
        .values_list("model", flat=True).distinct()
    )
    data_set_by_date = (
        Filtered_data.objects.exclude(model="etc")
        .values_list("date", flat=True).distinct()
    )
    for model in data_set_by_model:
        for date in data_set_by_date:
            filtered_data = Filtered_data.objects.filter(model=model, posted_at=date)
            average_price_data = average_price_func(filtered_data)
            input_fitered_data(average_price_data)
    return HttpResponse(status=200)
