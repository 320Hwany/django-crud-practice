import logging
from dataclasses import asdict
from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from crud_app.dependency_container import container
from crud_app.dtos.dtos import MemberCreateRequest, MemberResponse, MemberUpdateRequest

logger = logging.getLogger(__name__)

def handle_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return Response({"message": str(e)}, status=400)
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return Response({"message": "An error occurred"}, status=500)
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

class MemberListView(APIView):

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.member_service = container.member_service

    @handle_exception
    def get(self, request: Request, member_id: int) -> Response:
        member_response: MemberResponse = self.member_service.get_member(member_id)
        return Response(asdict(member_response), status=200)

    @handle_exception
    def patch(self, request: Request, member_id: int) -> Response:
        member_update_request: MemberUpdateRequest = MemberUpdateRequest(**request.data)
        self.member_service.update_member(member_id, member_update_request)
        return Response("OK", status=200)

    @handle_exception
    def delete(self, request: Request, member_id: int) -> Response:
        self.member_service.delete_member(member_id)
        return Response("OK", status=200)