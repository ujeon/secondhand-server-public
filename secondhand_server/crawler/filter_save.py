from django.http import HttpResponse
from .models import Raw_data, Filtered_data
from .filter_func import filter_func


def input_fitered_data(data):
    # REVIEW: 데이터를 크롤링 하고 DB에 저장합니다. 실패하면 except로 넘어갑니다.
    try:
        new_data = Filtered_data(
            brand=data["brand"],
            model=data["model"],
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
        # TOFIX: 어떤 에러인지 확인이 아래 코드로 가능합니다
    except Exception as ex:
        print('오류', ex)
        return HttpResponse(status=500)


# DB에서 raw data를 불러오는 함수
def retrieve_raw_data():
    data_set = Raw_data.objects.filter(
        price__gte=20000).values('title', 'content', 'price', 'url', 'img_url', 'market', 'posted_at', 'is_sold', 'location', 'category_id').order_by('url').distinct()

    for data in data_set:
        if data["price"] % 1000 == 0:
            filtered_data = filter_func(data)
            input_fitered_data(filtered_data)

    return
