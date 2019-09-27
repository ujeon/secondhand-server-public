import re
from product_dict import stroller_dictionary, pet_dictionary
from KoNLPy import konlpy_filter


def convertSpecialCharactersIntoSpace(string):
    newString = re.sub(
        r"[-=+_,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>\{\};`'…》]", " ", string
    )
    return newString


def splitStringIntoList(string):
    stringList = string.split(" ")
    while stringList.count(""):
        stringList.remove("")
    return stringList


def makeUsefulList(string):
    string = convertSpecialCharactersIntoSpace(string)
    return splitStringIntoList(string)


def brandAndModelIsNotInData(data):
    if (data.get("brand") == None) or (data.get("model") == None):
        return True
    return False


def filter_func(data):
    filtered_data = {
        # "price": data["price"],
        # "url": data["url"],
        # "img_url": data["img_url"],
        # "market": data["market"],
        # "posted_at": data["posted_at"],
        # "is_sold": data["is_sold"],
        # "category_id": data["category_id"],
        # "location": data["location"],
    }

    def matchBrandAndModel(list, brandAndModel):

        for name in list:
            for key in brandAndModel:
                if name in key:
                    filtered_data["brand"] = key[0]
                    for model in brandAndModel[key]:
                        if name in model:
                            filtered_data["model"] = model[0]
                            break
            if filtered_data.get("brand") == None:
                for key in brandAndModel:
                    for model in brandAndModel[key]:
                        if name in model:
                            filtered_data["brand"] = key[0]
                            filtered_data["model"] = model[0]
                            break

    title = makeUsefulList(data["title"])
    matchBrandAndModel(title, stroller_dictionary)
    print(1, filtered_data)
    if brandAndModelIsNotInData(filtered_data):
        content = makeUsefulList(data["content"])
        matchBrandAndModel(content, stroller_dictionary)
        print(2, filtered_data)
        if brandAndModelIsNotInData(filtered_data):
            titleList = konlpy_filter(" ".join(title))
            print(titleList)
            matchBrandAndModel(titleList, stroller_dictionary)
            print(3, filtered_data)
            if brandAndModelIsNotInData(filtered_data):
                contentList = ""
                if len(content) != 0:
                    contentList = konlpy_filter(" ".join(content))
                matchBrandAndModel(contentList, stroller_dictionary)
                print(4, filtered_data)

                if filtered_data.get("brand") == None:
                    print(contentList)
                    matchBrandAndModel(titleList, pet_dictionary)
                    if brandAndModelIsNotInData(filtered_data):
                        matchBrandAndModel(contentList, pet_dictionary)
                if filtered_data.get("model") == None:
                    print("!!")
                    filtered_data["model"] = "etc"
                if brandAndModelIsNotInData(filtered_data):
                    print("!!!")
                    filtered_data["brand"] = "etc"
                    filtered_data["model"] = "etc"

    return filtered_data


raw_data = {
    "title": "유모차 ,미니버기유모차,검정유모차,절충형유모차",
    "content": "최저가도 37만원대! 저도 롯*백화점에서 직접구매해서 사십얼마주고샀어요 ㅠㅠ ㅎ 제가 아이가 한명이라 한명아이만 쓴거구요 상태 좋아요 절충형이 짱이져 유모차는! 7살 전까지 탈수있다고 판매하시는분이 그러셨는대 전애기가 1월생5살이라 이제 유모차랑 안녕할가해요 앉은거랑 눕히는것도 가능하구요 제가 세탁해서 건조기까지 돌려서 뽀송 해졌다능!! 휴대도 간편하고 휴대용유모차보다 쿠션감이 짱이에요!! 블랙이라떼도 안타구요 ㅎ 직거래만 원해요 (예민하신분은 거래안합니다)",
}


print(filter_func(raw_data))
