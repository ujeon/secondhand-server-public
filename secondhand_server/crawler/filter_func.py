import re
from .product_dict import stroller_dictionary, pet_dictionary
from .KoNLPy import konlpy_filter


def convertSpecialCharactersIntoSpace(string):
    newString = re.sub(
        r"[-=+_,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>\{\};`'…》\n]", " ", string
    )
    before_emoji_clear = re.compile(
        '[\U00010000-\U0010ffff]', flags=re.UNICODE)
    newString = before_emoji_clear.sub(r'', newString)
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
        "price": data['price'],
        "url": data['url'],
        "img_url": data['img_url'],
        "market": data['market'],
        "posted_at": data['posted_at'],
        "is_sold": data['is_sold'],
        "category_id": data['category_id'],
        "location": data['location'],
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

    title = makeUsefulList(data['title'])
    matchBrandAndModel(title, stroller_dictionary)
    if brandAndModelIsNotInData(filtered_data):
        content = makeUsefulList(data['content'])
        matchBrandAndModel(content, stroller_dictionary)
        if brandAndModelIsNotInData(filtered_data):
            titleList = konlpy_filter(" ".join(title))
            matchBrandAndModel(titleList, stroller_dictionary)
            if brandAndModelIsNotInData(filtered_data):
                contentList = ""
                if len(content) != 0:
                    contentList = konlpy_filter(" ".join(content))
                matchBrandAndModel(contentList, stroller_dictionary)

                if filtered_data.get("brand") == None:
                    matchBrandAndModel(titleList, pet_dictionary)
                    if brandAndModelIsNotInData(filtered_data):
                        matchBrandAndModel(contentList, pet_dictionary)
                if filtered_data.get("model") == None:
                    filtered_data["model"] = "etc"
                if brandAndModelIsNotInData(filtered_data):
                    filtered_data["brand"] = "etc"
                    filtered_data["model"] = "etc"

    return filtered_data
