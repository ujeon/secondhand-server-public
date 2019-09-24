import requests, datetime, time, json


class Bungae_crawler:
    # REVIEW 인스턴스 생성할 때 전달받은 키워드를 self에 keyword로 저장합니다.
    def __init__(self, keyword):
        self.lists_url = "https://core-api.bunjang.co.kr/api/1/find.json?q={keyword}&order=date&n={num}&f_category_id=500"
        self.detail_url = "https://core-api.bunjang.co.kr/api/1/product/{product_id}/detail_info.json?stat_uid=&version=2"
        self.link_url = "https://m.bunjang.co.kr/products/{product_id}?ref=%EA%B2%80%EC%83%89%EA%B2%B0%EA%B3%BC&q={keyword}"
        self.keyword = keyword

    # REVIEW 데이터를 요청하여 가공한 후 가공한 데이터를 반환하는 함수
    def data_maker(self, count):
        result = []
        url = self.lists_url.format(num=count, keyword=self.keyword)
        req_lists = requests.get(url)
        parsed_lists = json.loads(req_lists.text)["list"]
        for data in parsed_lists:
            url2 = self.detail_url.format(product_id=data["pid"])
            req_detail = requests.get(url2)
            parsed_details = json.loads(req_detail.text)["item_info"]

            # TOFIX 현재 시간 - update_time을 계산하였는데, 딱히 정확한 것 같지는 않습니다.
            current_milli_time = lambda: int(round(time.time() * 1000))
            milli_sec = current_milli_time() - parsed_details["update_time"]
            date = datetime.datetime.fromtimestamp(milli_sec / 1000.0)
            date = date.strftime("%Y-%m-%d")

            # REVIEW 위치와 이미지는 존재하지 않을 가능성이 있으므로, 없는 경우에는 None으로 처리하였습니다.
            temp = {
                "title": parsed_details["name"],
                "content": parsed_details["description"],
                "url": self.link_url.format(
                    product_id=data["pid"], keyword=self.keyword
                ),
                "img_url": parsed_details["product_image"]
                if parsed_details["product_image"] != ""
                else None,
                "price": parsed_details["price"],
                "location": parsed_details["latitude"]
                + "-"
                + parsed_details["longitude"]
                if parsed_details["latitude"] != ""
                else None,
                "market": "번개장터",
                "posted_at": date,
            }
            result.append(temp)
        return result


# REVIEW 번개장터 크롤러 클래스에 찾고자 하는 카테고리 키워드를 전달합니다.
a = Bungae_crawler("유모차")

# REVIEW 가져올 데이터의 갯수를 전달합니다.
data = a.data_maker(10)
print(data)
