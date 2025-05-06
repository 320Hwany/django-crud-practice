import logging
from dataclasses import asdict
from functools import wraps
from typing import Any

import jwt
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from crud_app.dependency_container import container
from crud_app.dtos.dtos import MemberCreateRequest, MemberResponse, MemberUpdateRequest, MemberLoginRequest, JwtToken

logger = logging.getLogger(__name__)

def handle_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return Response({"message": str(e)}, status=400)
        except AuthenticationFailed as e:
            return Response({"message": str(e)}, status=401)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return Response({"message": "An error occurred"}, status=500)
    return wrapper

def authentication(func):
    @wraps(func)
    def wrapper(self, request: Request, *args, **kwargs):
        secret_key: str = "GZ8x8-Dl2FZAClDee7aOZ5rHnPDO1BtYK8wH6P5wf_k"
        algorithm: str = "HS256"

        access_token: str = request.headers.get("AccessToken")
        refresh_token: str = request.headers.get("RefreshToken")

        try:
            access_payload = jwt.decode(access_token, secret_key, algorithms=[algorithm])
            member_id = access_payload.get("member_id")
        except jwt.ExpiredSignatureError:
            try:
                refresh_payload = jwt.decode(refresh_token, secret_key, algorithms=[algorithm])
                member_id = refresh_payload.get("member_id")
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("Refresh token has expired")
            except jwt.InvalidTokenError:
                raise AuthenticationFailed("Invalid refresh token")
        except jwt.InvalidTokenError:
            raise AuthenticationFailed("Invalid access token")

        return func(self, request, member_id=member_id, *args, **kwargs)
    return wrapper

class MemberView(APIView):

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.member_service = container.member_service

    @handle_exception
    def post(self, request: Request) -> Response:
        member_create_request: MemberCreateRequest = MemberCreateRequest(**request.data)
        self.member_service.create_member(member_create_request)
        return Response("OK", status=201)

    @handle_exception
    @authentication
    def get(self, request: Request, member_id: int) -> Response:
        member_response: MemberResponse = self.member_service.get_member(member_id)
        return Response(asdict(member_response), status=200)

    @handle_exception
    @authentication
    def patch(self, request: Request, member_id: int) -> Response:
        member_update_request: MemberUpdateRequest = MemberUpdateRequest(**request.data)
        self.member_service.update_member(member_id, member_update_request)
        return Response("OK", status=200)

    @handle_exception
    @authentication
    def delete(self, request: Request, member_id: int) -> Response:
        self.member_service.delete_member(member_id)
        return Response("OK", status=200)

class MemberLoginView(APIView):

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.member_service = container.member_service

    @handle_exception
    def post(self, request: Request) -> Response:
        member_login_request: MemberLoginRequest = MemberLoginRequest(**request.data)
        jwt_token: JwtToken = self.member_service.login(member_login_request)
        return Response(asdict(jwt_token), status=200)