import requests
import json
import datetime
import os

from bs4 import BeautifulSoup
from urllib import parse
from django.core.exceptions import ImproperlyConfigured

# 시크릿 키가 담긴 파일 불러오는 함수
with open("secrets.json") as f:
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


def daangn_crawler(page):
    # 추후 데이터베이스에서 가져온 카테고리 리스트 사용
    category = ["유모차"]
    eachItemAddress = {}
    for i in category:
        for k in range(1, page):
            req = requests.get(
                f"https://www.daangn.com/search/{i}/more/flea_market?page={k}"
            )
            html = req.text
            soup = BeautifulSoup(html, "html.parser")
            addressList = []
            for link in soup.select("article > a"):
                addressList.append(link.attrs["href"])
                eachItemAddress[str(k)] = addressList

    result = []
    for page in eachItemAddress:
        for link in eachItemAddress[page]:
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
                raw_data["img_url"] = None
            result.append(raw_data)
    print(result)
    return result


daangn_crawler(2)
