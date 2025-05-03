from datetime import datetime
from dataclasses import dataclass, field

import pytz

from crud_app.dtos.dtos import MemberCreateRequest


@dataclass(kw_only=True, eq=True, frozen=True)
class MemberEntity:
    name: str
    email: str
    age: int

    @staticmethod
    def to_entity(member_create_request: MemberCreateRequest) -> "MemberEntity":
        return MemberEntity(
            name=member_create_request.name,
            email=member_create_request.email,
            age=member_create_request.age,
        )

@dataclass(kw_only=True, eq=True, frozen=True)
class OrderEntity:
    order_id: int
    member_id: int
    price: str
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=pytz.timezone("Asia/Seoul")))
    updated_at: datetime = field(default_factory=lambda: datetime.now(tz=pytz.timezone("Asia/Seoul")))