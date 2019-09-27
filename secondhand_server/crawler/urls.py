from django.urls import path

from . import views
from . import filter_save

urlpatterns = [
    path("eachModelInfo/<str:brand>/<str:model>/info/",
         views.handle_each_model_info),
    path("search/", views.handle_search_price),
    path("all/", views.search_route_brand_model),
    path("allCategories/", views.get_categories),
    path("category/<str:category>/brand/", views.get_brands),
    path("category/<str:category>/brand/<str:brand>/model/", views.get_models),
    path("input/data/", views.input_bungae_data),
    path("input/filter/", filter_save.retrieve_raw_data)
]


# 한글로 검색 시, url주소를 클라이언트에서 이스케이프해줘야 오류 발생을 막을 수 있음.
# http://mwultong.blogspot.com/2006/10/urlencode-encoding-javascript.html
