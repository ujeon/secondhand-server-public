# FIXED 데이터 베이스에 (아마도?) 전부 Null 허용이 안되어서 뭐라도 값이 들어가야 할 것 같아요. 전부 "-"로 수정했습니다.
# FIXED 기본적으로 가져오는 데이터(페이지) default 설정해놨습니다.

import requests
import json
import datetime
import os

from bs4 import BeautifulSoup
from urllib import parse
from django.core.exceptions import ImproperlyConfigured
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


def daangn_crawler(page=10):
    # 추후 데이터베이스에서 가져온 카테고리 리스트 사용
    category = ["유모차"]
    link_list = []
    filtered_url_list = Filtered_data.objects.filter(market="당근마켓").values_list(
        "url", flat=True
    )
    for i in category:
        for k in range(1, page + 1):
            req = requests.get(
                f"https://www.daangn.com/search/{i}/more/flea_market?page={k}"
            )
            html = req.text
            soup = BeautifulSoup(html, "html.parser")
            for link in soup.select("article > a"):
                full_link = "https://www.daangn.com" + link.attrs["href"]
                if (
                    full_link not in filtered_url_list
                    and link.attrs["href"] not in link_list
                ):
                    link_list.append(link.attrs["href"])

        for link in link_list:
            try:
                req = requests.get(f"https://www.daangn.com{link}")
                html = req.text
                soup = BeautifulSoup(html, "html.parser")

                raw_data = {
                    "title": soup.select("#article-title")[0].text,
                    "content": soup.select("#article-detail")[0]
                    .text.replace("\n", " ")
                    .strip(),
                    "url": f"https://www.daangn.com{link}",
                    "market": "당근마켓",
                    "is_sold": False,
                    "category_id": 1,
                }

                location = getCoordinate(soup.select("#region-name")[0].text)
                raw_data["location"] = location

                dateCheck = soup.select("#article-category > time")[0].text
                if ("일" in dateCheck) == False:
                    raw_data["posted_at"] = datetime.datetime.now().date()
                else:
                    postedAt = soup.select("#article-category > time")[0].text.replace(
                        "일 전", ""
                    )
                    raw_data["posted_at"] = (
                        datetime.date.today() - datetime.timedelta(days=int(postedAt))
                    ).strftime("%Y-%m-%d")

                if (
                    len(soup.select("#article-price")) == 0
                    or soup.select("#article-price")[0].text.replace("\n", "").strip()[-1]
                    != "원"
                ):
                    raw_data["price"] = 0
                else:
                    price = soup.select("#article-price")[0].text
                    toBeReplaces = ["\n", "원", ","]
                    for el in toBeReplaces:
                        if el in price:
                            price = price.replace(el, "")
                    raw_data["price"] = int(price.strip())

                if len(soup.select("div.image-wrap > img")) > 0:
                    raw_data["img_url"] = soup.select("div.image-wrap > img")[0].attrs[
                        "data-lazy"
                    ]
                else:
                    raw_data["img_url"] = "-"
                input_crawl_data(raw_data)
            except Exception as err:
                print(err)
                pass
    return print(" 당근마켓 크롤링 완료")
