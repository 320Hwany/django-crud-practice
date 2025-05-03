import logging
from typing import Any

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from crud_app.dependency_container import container
from crud_app.dtos.dtos import MemberCreateRequest

logger = logging.getLogger(__name__)

class MemberView(APIView):

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.member_service = container.member_service

    def post(self, request: Request) -> Response:
        member_create_request = MemberCreateRequest(
            name=request.data.get("name", ""),
            email=request.data.get("email", ""),
            age=request.data.get("age", 0),
        )
        self.member_service.create_member(member_create_request)
        return Response("OK", status=201)