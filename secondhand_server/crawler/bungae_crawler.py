import requests
import datetime
import time
import json
from selenium import webdriver
from bs4 import BeautifulSoup
from .raw_data_save import input_crawl_data
from .models import Filtered_data


class Bungae_crawler:
    # REVIEW 인스턴스 생성할 때 전달받은 키워드를 self에 keyword로 저장합니다.
    def __init__(self, keyword):
        self.lists_url = "https://core-api.bunjang.co.kr/api/1/find.json?q={keyword}&order=date&n={num}"
        self.detail_url = "https://core-api.bunjang.co.kr/api/1/product/{product_id}/detail_info.json?stat_uid=&version=2"
        self.link_url = "https://m.bunjang.co.kr/products/{product_id}?ref=%EA%B2%80%EC%83%89%EA%B2%B0%EA%B3%BC&q={keyword}"
        self.keyword = keyword

    # REVIEW 데이터를 요청하여 가공한 후 가공한 데이터를 반환하는 함수
    def data_maker(self, count=50):
        options = webdriver.ChromeOptions()
        options.add_argument("headless")
        options.add_argument("disable-gpu")

        driver = webdriver.Chrome(
            "/Users/khwi/Downloads/chromedriver", chrome_options=options
        )

        url = self.lists_url.format(num=count, keyword=self.keyword)
        req_lists = requests.get(url)
        parsed_lists = json.loads(req_lists.text)["list"]

        filtered_url_list = Filtered_data.objects.filter(market="번개장터").values_list(
            "url", flat=True
        )

        for data in parsed_lists:
            try:
                url2 = self.detail_url.format(product_id=data["pid"])
                link_url = self.link_url.format(
                    product_id=data["pid"], keyword=self.keyword
                )
                req_detail = requests.get(url2)
                parsed_details = json.loads(req_detail.text)["item_info"]

                driver.get(link_url)

                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                # REVIEW 게시글 업데이트 시간을 HTML 엘리먼트에서 가져와서 해당 시간 데이터 처리
                update_time = soup.find("span", {"class": "text-time"}).text
                update_time = update_time.split()[0]

                # REVIEW 현재시간을 millisecond로 계산할 수 있도록 하는 함수.
                def current_milli_time():
                    return int(round(time.time() * 1000))

                if "시간" in update_time:
                    update_time = update_time.split("시간")[0]
                    update_time = int(update_time) * 3600000
                    time_gap = current_milli_time() - update_time
                    date = datetime.datetime.fromtimestamp(time_gap / 1000.0)
                elif "일" in update_time:
                    update_time = update_time.split("일")[0]
                    update_time = int(update_time) * 86400000
                    time_gap = current_milli_time() - update_time
                    date = datetime.datetime.fromtimestamp(time_gap / 1000.0)
                elif "주" in update_time:
                    update_time = update_time.split("주")[0]
                    update_time = int(update_time) * 604800000
                    time_gap = current_milli_time() - update_time
                    date = datetime.datetime.fromtimestamp(time_gap / 1000.0)
                elif "달" in update_time:
                    update_time = update_time.split("달")[0]
                    update_time = int(update_time) * 604800000 * 4
                    time_gap = current_milli_time() - update_time
                    date = datetime.datetime.fromtimestamp(time_gap / 1000.0)
                else:
                    date = datetime.datetime.fromtimestamp(
                        current_milli_time() / 1000.0)

                date = date.strftime("%Y-%m-%d")

                raw_data = {
                    "title": parsed_details["name"],
                    "content": parsed_details["description"],
                    "url": link_url,
                    "img_url": parsed_details["product_image"]
                    if parsed_details["product_image"] != ""
                    else "-",
                    "price": parsed_details["price"],
                    "location": parsed_details["latitude"]
                    + "-"
                    + parsed_details["longitude"]
                    if parsed_details["latitude"] != ""
                    else "-",
                    "market": "번개장터",
                    "posted_at": date,
                    "is_sold": True if parsed_details["status"] == 3 else False,
                    "category_id": 1,
                }

                if raw_data["url"] not in filtered_url_list:
                    input_crawl_data(raw_data)
            except Exception as err:
                print(err)
                pass

        driver.quit()
        return print("번개장터 크롤링 완료")
