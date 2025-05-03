from dataclasses import dataclass


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