from dataclasses import dataclass

from crud_app.models import Member


@dataclass(kw_only=True, eq=True, frozen=True)
class MemberCreateRequest:
    name: str
    email: str
    age: int

    def __post_init__(self):
        if not self.name or self.name.strip() == "":
            raise ValueError("이름을 입력해주세요.")
        if not self.email or self.email.strip() == "":
            raise ValueError("이메일을 입력해주세요.")
        if self.age <= 0:
            raise ValueError("나이를 입력해주세요.")

    def to_model(self) -> 'Member':
        return Member(
            name=self.name,
            email=self.email,
            age=self.age
        )


@dataclass(kw_only=True, eq=True, frozen=True)
class MemberResponse:
    member_id: int
    name: str
    email: str
    age: int

    @staticmethod
    def from_model(member: Member) -> 'MemberResponse':
        return MemberResponse(
            member_id=member.member_id,
            name=member.name,
            email=member.email,
            age=member.age
        )
