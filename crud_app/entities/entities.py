from datetime import datetime
from dataclasses import dataclass, field

import pytz



@dataclass(kw_only=True, eq=True, frozen=True)
class MemberEntity:
    name: str
    email: str
    age: int


@dataclass(kw_only=True, eq=True, frozen=True)
class OrderEntity:
    order_id: int
    member_id: int
    price: str
    created_at: datetime = field(default_factory=lambda: datetime.now(tz=pytz.timezone("Asia/Seoul")))
    updated_at: datetime = field(default_factory=lambda: datetime.now(tz=pytz.timezone("Asia/Seoul")))