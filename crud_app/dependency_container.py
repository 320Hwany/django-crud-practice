from crud_app.repository.member_repository import MemberRepository
from crud_app.service.member_service import MemberService


class DependencyContainer:
    def __init__(self):
        self._member_repository = MemberRepository()
        self._member_service = MemberService(self._member_repository)

    @property
    def member_repository(self) -> MemberRepository:
        return self._member_repository

    @property
    def member_service(self) -> MemberService:
        return self._member_service

container = DependencyContainer()