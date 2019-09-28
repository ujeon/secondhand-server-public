# FIXED 데이터 베이스에 (아마도?) 전부 Null 허용이 안되어서 뭐라도 값이 들어가야 할 것 같아요. 전부 "-"로 수정했습니다.

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib import parse
from django.core.exceptions import ImproperlyConfigured
import datetime
import re
import json
import requests
import os
from .raw_data_save import input_crawl_data
from .models import Filtered_data

# 시크릿 키가 담긴 파일 불러오는 함수
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

secret_file = os.path.join(BASE_DIR, "secret.json")


with open(secret_file) as f:
    secret = json.loads(f.read())


def get_secret(setting, secret=secret):
    try:
        return secret[setting]
    except:
        error_msg = "Set key '{0}' in secret.json".format(setting)
        raise ImproperlyConfigured(error_msg)


# 필요한 시크릿 키는 아래와 같이 변수에 담아서 사용
NAVER_API_ID = get_secret("NAVER_API_ID")
NAVER_API_KEY = get_secret("NAVER_API_KEY")


def getCoordinate(query):
    encodedQuery = parse.quote(query)
    headers = {
        "X-NCP-APIGW-API-KEY-ID": NAVER_API_ID,
        "X-NCP-APIGW-API-KEY": NAVER_API_KEY,
    }
    req = requests.get(
        f"https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={encodedQuery}",
        headers=headers,
    )
    locationBody = json.loads(req.text)
    location = (
        f'{locationBody["addresses"][0]["y"]}-{locationBody["addresses"][0]["x"]}'
    )
    return location


def retrieve_filtered_data():
    url_list = Filtered_data.objects.filter(
        market="헬로마켓"
    ).values_list('url', flat=True)
    return url_list


def hello_crawler(number):
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    options.add_argument("window-size=1920x1080")
    options.add_argument("disable-gpu")
    options.add_argument("lang=ko_KR")  # 한국어

    # UserAgent 변경
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
    )

    driver = webdriver.Chrome(
        "/Users/khwi/Downloads/chromedriver", chrome_options=options
    )

    url_list = retrieve_filtered_data()
    item_number_list = []

    for num in range(1, number + 1):
        TEST_URL = f"https://www.hellomarket.com/search?q=%EC%9C%A0%EB%AA%A8%EC%B0%A8&page={num}"
        driver.get(TEST_URL)

        # headless 탐지 방어 위한 코드
        driver.execute_script(
            "Object.defineProperty(navigator, 'plugins', {get: function() {return[1, 2, 3, 4, 5]}})"
        )
        driver.execute_script(
            "Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})"
        )
        driver.execute_script(
            "const getParameter = WebGLRenderingContext.getParameter;WebGLRenderingContext.prototype.getParameter = function(parameter) {if (parameter === 37445) {return 'NVIDIA Corporation'} if (parameter === 37446) {return 'NVIDIA GeForce GTX 980 Ti OpenGL Engine';}return getParameter(parameter);};"
        )

        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        image_url = soup.select("div.list_area > div > ul > li > a")

        for url in image_url:
            item_href = url.get("href")
            item_number = item_href[6:]
            if item_number not in item_number_list:
                item_number_list.append(item_number)

    for item_number in item_number_list:
        raw_data = {}
        try:
            driver.get("https://www.hellomarket.com/item/%s" % item_number)
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            raw_data["title"] = soup.select("div.item_info > span")[0].text
            raw_data["content"] = (
                soup.select("div.description_text")[
                    0].text.replace("\n", " ").strip()
            )
            price_string = soup.select("div.item_price.item_price_bottom")[
                0].text[:-1]

            if price_string.replace(",", "").isdigit():
                raw_data["price"] = int(price_string.replace(",", ""))
            else:
                raw_data["price"] = 0
            raw_data["url"] = "https://www.hellomarket.com/item/%s" % item_number
            raw_data["img_url"] = soup.select(
                "img.view.thumbnail_img")[0].attrs["src"]
            raw_data["market"] = "헬로마켓"
            posted_at_text = soup.select("div.item_addr_area > span")[0].text
            posted_at = ""

            if (
                posted_at_text.find("분") != -1
                or posted_at_text.find("시간") != -1
                or posted_at_text.find("초") != -1
            ):
                posted_at = datetime.datetime.now().date()
            elif posted_at_text.find("일") != -1:
                day_int = int(posted_at_text.replace("일전", ""))
                posted_at = datetime.date.today() - datetime.timedelta(days=day_int)
            else:
                reg_exr = re.compile(r"[0-9]*\d\b")
                num = reg_exr.findall(posted_at_text)
                date_string = "2019-"
                if len(num[0]) == 1:
                    date_string = date_string + "0" + num[0] + "-" + num[1]
                    posted_at = datetime.datetime.strptime(
                        date_string, "%Y-%m-%d").date()
                else:
                    date_string = date_string + num[0] + "-" + num[1]
                    posted_at = datetime.datetime.strptime(
                        date_string, "%Y-%m-%d").date()
            raw_data["posted_at"] = posted_at
            raw_data["is_sold"] = False
            raw_data["category_id"] = 1
            # FIXED 데이터 베이스에 location이 필수로 되어 있습니다. 수정할게요
            location = ""
            location_string = soup.select("div.item_addr_area > span")[1].text
            if location_string == "판매자가 위치를 지정하지 않았습니다.":
                location = "-"  # None => "-"
            else:
                location = getCoordinate(location_string)
            raw_data["location"] = location

            if raw_data["url"] not in url_list:
                input_crawl_data(raw_data)
                print('크롤링 중')
            else:
                print('크롤링 완료')
                return
        except Exception as err:
            print(err)
            pass
        # json_type_text.append(raw_data)

    driver.quit()
    return
