from crud_app.dtos.dtos import MemberCreateRequest
from crud_app.models import Member


class MemberRepository:

    def create_member(self, dto: MemberCreateRequest) -> None:
        member = dto.to_model()
        member.save()

    def get_member(self, member_id):
        return Member.objects.get(member_id=member_id)

    def update_member(self, member_id, member_data):
        """
        Update an existing member's information.
        """
        # Implementation for updating a member
        pass

    def delete_member(self, member_id):
        """
        Delete a member from the database.
        """
        # Implementation for deleting a member
        pass