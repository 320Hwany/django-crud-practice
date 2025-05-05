from dataclasses import asdict

from django.db import transaction

from crud_app.dtos.dtos import MemberCreateRequest, MemberUpdateRequest, MemberLoginRequest, JwtToken
from crud_app.models import Member, JwtRefreshToken

import jwt
from datetime import datetime, timedelta


class MemberRepository:

    @transaction.atomic
    def create_member(self, dto: MemberCreateRequest) -> Member:
        member = dto.to_model()
        member.save()
        return member

    @transaction.atomic
    def login(self, dto: MemberLoginRequest) -> JwtToken:
        try:
            member = Member.objects.get(email=dto.email, password=dto.password)

            access_payload = {
                "member_id": member.member_id,
                "name": member.name,
                "email": member.email,
                "age": member.age,
                "exp": datetime.utcnow() + timedelta(hours=1)  # access_token 만료 시간 (1시간)
            }
            refresh_payload = {
                "member_id": member.member_id,
                "exp": datetime.utcnow() + timedelta(hours=24)  # refresh_token 만료 시간 (24시간)
            }
            secret_key: str = "GZ8x8-Dl2FZAClDee7aOZ5rHnPDO1BtYK8wH6P5wf_k"
            access_token: str = jwt.encode(access_payload, secret_key, algorithm="HS256")
            refresh_token: str = jwt.encode(refresh_payload, secret_key, algorithm="HS256")

            jwt_refresh_token: JwtRefreshToken = JwtRefreshToken(member_id=member.member_id, refresh_token=refresh_token)
            jwt_refresh_token.save()

            return JwtToken(access_token=access_token, refresh_token=refresh_token)

        except Member.DoesNotExist:
            raise ValueError("회원 정보가 존재하지 않습니다.")

    @transaction.atomic
    def get_member(self, member_id: int) -> Member:
        try :
            return Member.objects.get(member_id=member_id)
        except Member.DoesNotExist:
            raise ValueError(f"회원 id가 {member_id}인 회원이 존재하지 않습니다.")

    @transaction.atomic
    def update_member(self, member_id: int, dto: MemberUpdateRequest) -> None:
        try:
            member = Member.objects.get(member_id=member_id)
            for field, value in asdict(dto).items():
                setattr(member, field, value)
            member.save()
        except Member.DoesNotExist:
            raise ValueError(f"회원 id가 {member_id}인 회원이 존재하지 않아 수정할 수 없습니다.")

    @transaction.atomic
    def delete_member(self, member_id) -> None:
        try:
            member = Member.objects.get(member_id=member_id)
            member.delete()
        except Member.DoesNotExist:
            raise ValueError(f"회원 id가 {member_id}인 회원이 존재하지 않아 삭제할 수 없습니다.")