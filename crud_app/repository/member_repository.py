from dataclasses import asdict

from django.contrib.sessions.backends.base import SessionBase
from django.db import transaction
from rest_framework import request

from crud_app.dtos.dtos import MemberCreateRequest, MemberUpdateRequest, MemberLoginRequest
from crud_app.models import Member


class MemberRepository:

    @transaction.atomic
    def create_member(self, dto: MemberCreateRequest) -> Member:
        member = dto.to_model()
        member.save()
        return member

    @transaction.atomic
    def login(self, dto: MemberLoginRequest, session: SessionBase) -> Member:
        try:
            if 'member_id' in request.session:
                member_id = request.session['member_id']
                member: Member = Member.objects.get(member_id=member_id)
            else:
                member: Member = Member.objects.get(email=dto.email, password=dto.password)
                session['member_id'] = member.member_id

            return member
        except Member.DoesNotExist:
            raise ValueError(f"회원 정보가 일치하지 않습니다.")

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