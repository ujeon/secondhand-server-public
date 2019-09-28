from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Favorite


from crawler.models import Filtered_data
from django.http import JsonResponse
import json
import os
import time


from .encrypt import AESCipher
from django.db.models import Q
from django.utils import timezone
from authlib.jose import jwt


from django.core.exceptions import ImproperlyConfigured

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


SECRET_JWT = get_secret("SECRET_JWT")


def handle_user_signup(request):
    request_body = json.loads(request.body)

    user_data = User.objects.filter(
        Q(email=request_body["email"]) | Q(nickname=request_body["nickname"])
    ).values("email", "nickname")

    result = {}

    for data in user_data:
        if data["email"] == request_body["email"]:
            result["message"] = "이미 존재하는 이메일이에요."
            return HttpResponse(JsonResponse(result))
        elif data["nickname"] == request_body["nickname"]:
            result["message"] = "이미 존재하는 닉네임이에요. 다시 설정해주세요."
            return HttpResponse(JsonResponse(result))

    new_user = User(
        email=request_body["email"],
        nickname=request_body["nickname"],
        password=AESCipher().encrypt_str(request_body["password"]),
    )

    new_user.save()
    result["message"] = "세컨 핸드에 가입하신 것을 축하드려요 :)"
    return HttpResponse(JsonResponse(result), status=200)


def handle_user_signin(request):
    request_body = json.loads(request.body)

    user_data = User.objects.filter(email=request_body["email"]).values(
        "id", "email", "password"
    )

    result = {}

    for data in user_data:

        hashed_pwd = AESCipher().decrypt_str(data["password"])
        if data["email"] != request_body["email"]:
            result["message"] = "이메일 주소가 일치하지 않습니다."
            return HttpResponse(JsonResponse(result))
        elif hashed_pwd != request_body["password"]:
            result["message"] = "비밀번호가 일치하지 않습니다."
            return HttpResponse(JsonResponse(result))
        elif (
            data["email"] == request_body["email"]
            and hashed_pwd == request_body["password"]
        ):
            header = {"alg": "HS256", "typ": "JWT"}
            payload = {
                "iss": "jellyfish",
                "exp": 3000000,
                "iat": int(round(time.time() * 1000)),
                "user_id": data["id"],
            }

            secret_JWT = SECRET_JWT
            token = jwt.encode(header, payload, secret_JWT)
            response = HttpResponse(status=200)
            response["token"] = token

            return response


def handle_userinfo(request):
    request_body = json.loads(request.body)

    claims = jwt.decode(request.headers["token"], SECRET_JWT)
    user_id = claims["user_id"]

    user = User.objects.get(id=user_id)

    if user:

        result = {}
        user_data = User.objects.get(id=request_body["user_id"])
        result["id"] = user_data.__dict__["id"]
        result["email"] = user_data.__dict__["email"]
        result["nickname"] = user_data.__dict__["nickname"]
        result["signup_date"] = user_data.__dict__["signup_date"]

        favorite_data = (
            Favorite.objects.filter(user=request_body["user_id"])
            .values("filtered_data_id")
            .order_by()
        )
        result["favorites"] = []
        for data in favorite_data:
            filtered_data = Filtered_data.objects.filter(
                id=data["filtered_data_id"]
            ).values()
            for favorite in filtered_data:
                result["favorites"].append(favorite)

        return HttpResponse(JsonResponse(result))

    else:
        return HttpResponse(status=404)


# favorite 리스트에 어떤 데이터를 내려줄지 한 번 다같이 고민해보기
def handle_user_favorite(request):
    request_body = json.loads(request.body)

    favorite_data = Favorite.objects.filter(
        user=request_body["user_id"], filtered_data_id=request_body["list_id"]
    ).values("user", "filtered_data_id")

    if favorite_data:
        Favorite.objects.filter(
            user=request_body["user_id"], filtered_data_id=request_body["list_id"]
        ).delete()
    else:
        new_favorite = Favorite(
            user=User.objects.get(id=request_body["user_id"]),
            filtered_data_id=request_body["list_id"],
        )
        new_favorite.save()

    return HttpResponse(status=200)

