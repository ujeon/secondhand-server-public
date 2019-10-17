from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Favorite
from .jwt_auth import token_generator, decode_token

from crawler.models import Filtered_data
from django.http import JsonResponse
import json
import time


from .encrypt import AESCipher
from django.db.models import Q
from django.utils import timezone
from authlib.jose import jwt

# POST
def handle_user_signup(request):
    request_body = json.loads(request.body)

    user_data = User.objects.filter(
        Q(email=request_body["email"]) | Q(nickname=request_body["nickname"])
    ).values("email", "nickname")

    result = {}

    for data in user_data:
        if (
            data["email"] == request_body["email"]
            and data["nickname"] == request_body["nickname"]
        ):
            result["emailErrMsg"] = "이미 존재하는 이메일이에요."
            result["nickErrMsg"] = "이미 존재하는 닉네임이에요."
            return HttpResponse(JsonResponse(result))
        elif data["email"] == request_body["email"]:
            result["emailErrMsg"] = "이미 존재하는 이메일이에요."
            return HttpResponse(JsonResponse(result))
        elif data["nickname"] == request_body["nickname"]:
            result["nickErrMsg"] = "이미 존재하는 닉네임이에요."
            return HttpResponse(JsonResponse(result))

    new_user = User(
        email=request_body["email"],
        nickname=request_body["nickname"],
        password=AESCipher().encrypt_str(request_body["password"]),
    )

    new_user.save()
    result["message"] = "세컨 핸드에 가입하신 것을 축하드려요 :)"
    return HttpResponse(JsonResponse(result), status=200)


# POST
def handle_user_signin(request):
    request_body = json.loads(request.body)

    user_data = User.objects.filter(email=request_body["email"]).values(
        "id", "email", "password"
    )

    result = {}

    for data in user_data:

        hashed_pwd = AESCipher().decrypt_str(data["password"])
        if (
            data["email"] != request_body["email"]
            or hashed_pwd != request_body["password"]
        ):
            result["message"] = "false"
            return HttpResponse(JsonResponse(result), status=403)

        elif (
            data["email"] == request_body["email"]
            and hashed_pwd == request_body["password"]
        ):
            token = token_generator("user_id", data["id"])
            result["message"] = "true"

            response = HttpResponse(JsonResponse(result), status=200)
            response["token"] = token

            return response


# GET
def handle_userinfo(request):
    token = request.headers["token"]
    claims = decode_token(token)
    user_id = claims["user_id"]

    user = User.objects.get(id=user_id)

    if user:
        result = {}
        user_data = User.objects.get(id=user_id)
        result["id"] = user_data.__dict__["id"]
        result["email"] = user_data.__dict__["email"]
        result["nickname"] = user_data.__dict__["nickname"]
        result["signup_date"] = user_data.__dict__["signup_date"]

        return HttpResponse(JsonResponse(result), status=200)
    else:
        return HttpResponse(status=403)


# GET favorite/info
def handle_user_favorite_info(request):
    token = request.headers["token"]
    claims = decode_token(token)
    user_id = claims["user_id"]

    user_favorite = Favorite.objects.filter(user=user_id).values()
    result = []
    for data in user_favorite:
        user_favorite_list = Filtered_data.objects.filter(
            id=data["filtered_data_id"]
        ).values()[0]
        result.append(user_favorite_list)

    return HttpResponse(JsonResponse(result, safe=False), status=200)


# favorite 리스트에 어떤 데이터를 내려줄지 한 번 다같이 고민해보기


def handle_user_favorite(request):
    request_body = json.loads(request.body)

    token = request.headers["token"]
    claims = decode_token(token)
    user_id = claims["user_id"]

    favorite_data = Favorite.objects.filter(
        user=user_id, filtered_data_id=request_body["list_id"]
    ).values("user", "filtered_data_id")

    if favorite_data:
        Favorite.objects.filter(
            user=user_id, filtered_data_id=request_body["list_id"]
        ).delete()
    else:
        new_favorite = Favorite(
            user=User.objects.get(id=user_id), filtered_data_id=request_body["list_id"]
        )
        new_favorite.save()

    user_favorite = Favorite.objects.filter(user=user_id).values()
    result = []
    for data in user_favorite:
        user_favorite_list = Filtered_data.objects.filter(
            id=data["filtered_data_id"]
        ).values()[0]
        result.append(user_favorite_list)

    return HttpResponse(JsonResponse(result, safe=False), status=200)


def check_user_auth(request):
    token = request.headers["token"]
    if token == "null":
        return HttpResponse(status=403)

    claims = decode_token(token)
    print(claims)
    print(
        (float(claims["exp"]) + float(claims["iat"])) < int(round(time.time() * 1000))
    )
    if claims:
        if claims["iss"] != "jellyfish":
            return HttpResponse(status=403)
        if (float(claims["exp"]) + float(claims["iat"])) < int(
            round(time.time() * 1000)
        ):
            return HttpResponse(status=403)
    else:
        return HttpResponse(status=403)

    return HttpResponse(status=200)
