from dataclasses import asdict

from crud_app.dtos.dtos import MemberCreateRequest, MemberUpdateRequest
from crud_app.models import Member


class MemberRepository:

    def create_member(self, dto: MemberCreateRequest) -> None:
        member = dto.to_model()
        member.save()

    def get_member(self, member_id):
        return Member.objects.get(member_id=member_id)

    def update_member(self, member_id: int, dto: MemberUpdateRequest) -> None:
        member = Member.objects.get(member_id=member_id)
        for field, value in asdict(dto).items():
            setattr(member, field, value)
        member.save()

    def delete_member(self, member_id):
        """
        Delete a member from the database.
        """
        # Implementation for deleting a member
        pass