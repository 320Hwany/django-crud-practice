from crud_app.dtos.dtos import MemberCreateRequest
from crud_app.repository.member_repository import MemberRepository


class MemberService:

    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def create_member(self, dto: MemberCreateRequest) -> None:
        self.member_repository.create_member(dto)