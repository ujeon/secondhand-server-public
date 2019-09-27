from django.shortcuts import render
from django.http import HttpResponse
from .models import User
from django.http import JsonResponse
import json

from .encrypt import AESCipher
from django.db.models import Q


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
        "email", "password"
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

    return HttpResponse(status=200)
