from django.http import HttpResponse
from .models import Raw_data, Filtered_data
# filter function에서 처리된 dict 저장 함수


def input_fitered_data(all_data):
    # REVIEW: 데이터를 크롤링 하고 DB에 저장합니다. 실패하면 except로 넘어갑니다.
    try:
        for data in all_data:
            new_data = Filtered_data(
                brand=data["title"],
                model=data["content"],
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


# DB에서 raw data를 불러오는 함수
def retrieve_raw_data(request):
    data_set = Raw_data.objects.all()
    for data in data_set:
        filtered_data = filter_func(data)
        input_fitered_data(filtered_data)

# 다른 파일에서 filter_func를 만들어서 불러 올 예정
