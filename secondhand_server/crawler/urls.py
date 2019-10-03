from django.urls import path

from . import views, filter_save, average_price_save, average_price_monthly, average_top5

urlpatterns = [
    path("<str:brand>/<str:model>/info/",
         views.handle_each_model_info),
    path("search/", views.handle_search_price),
    path("list/", views.search_route_brand_model),
    path("category/", views.get_categories),
    path("category/<str:category>/brand/", views.get_brands),
    path("category/<str:category>/<str:brand>/model/", views.get_models),
    path("top5/", average_top5.average_top5),
    path("average/monthly/", average_price_monthly.average_price_monthly),
    # path("input/data/", views.multi_crawl_save),
    # path("input/filter/", filter_save.retrieve_raw_data),
    # path("input/average/", average_price_save.retrieve_filtered_data),
    path("save_auto/", views.save_all_auto),
]


# 한글로 검색 시, url주소를 클라이언트에서 이스케이프해줘야 오류 발생을 막을 수 있음.
# http://mwultong.blogspot.com/2006/10/urlencode-encoding-javascript.html
