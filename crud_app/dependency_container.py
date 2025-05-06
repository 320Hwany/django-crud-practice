from typing import Any

from crud_app.repository.member_repository import MemberRepository
from crud_app.service.member_service import MemberService


class MetaSingleton(type):
    _instances: dict = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> object:
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class DependencyContainer(metaclass=MetaSingleton):
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