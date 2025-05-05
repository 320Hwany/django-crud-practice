from crud_app.dtos.dtos import MemberCreateRequest, MemberResponse, MemberUpdateRequest, MemberLoginRequest, JwtToken
from crud_app.models import Member
from crud_app.repository.member_repository import MemberRepository


class MemberService:

    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def create_member(self, dto: MemberCreateRequest) -> None:
        self.member_repository.create_member(dto)

    def login(self, dto: MemberLoginRequest) -> JwtToken:
        return self.member_repository.login(dto)

    def get_member(self, member_id: int) -> MemberResponse:
        member: Member = self.member_repository.get_member(member_id)
        return MemberResponse.from_model(member)

    def update_member(self, member_id: int, dto: MemberUpdateRequest) -> None:
        self.member_repository.update_member(member_id, dto)

    def delete_member(self, member_id: int) -> None:
        self.member_repository.delete_member(member_id)