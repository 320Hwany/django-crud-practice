import pytest

from crud_app.dtos.dtos import MemberCreateRequest, MemberUpdateRequest, MemberLoginRequest, JwtToken
from crud_app.models import Member, JwtRefreshToken
from crud_app.service.member_service import MemberService
from crud_app.repository.member_repository import MemberRepository

@pytest.mark.django_db
def test_create_member():
    # given
    member_repository = MemberRepository()
    member_service = MemberService(member_repository=member_repository)
    dto = MemberCreateRequest(
        name="test name",
        email="test@gmail.com",
        password="test password",
        age=20,
    )

    # when
    member_service.create_member(dto)

    # then
    assert Member.objects.filter().count() == 1

@pytest.mark.django_db
def test_login():
    # given
    member_repository = MemberRepository()
    member_service = MemberService(member_repository=member_repository)
    dto = MemberCreateRequest(
        name="test name",
        email="test@gmail.com",
        password="test password",
        age=20,
    )
    member: Member = member_repository.create_member(dto)

    member_login_request: MemberLoginRequest = MemberLoginRequest(email="test@gmail.com", password="test password", )

    # when
    jwt_token: JwtToken = member_service.login(member_login_request)

    # then
    assert jwt_token.access_token is not None
    assert jwt_token.refresh_token is not None

@pytest.mark.django_db
def test_login_fail():
    # given
    member_repository = MemberRepository()
    member_service = MemberService(member_repository=member_repository)
    dto = MemberCreateRequest(
        name="test name",
        email="test@gmail.com",
        password="test password",
        age=20,
    )
    member: Member = member_repository.create_member(dto)

    member_login_request: MemberLoginRequest = MemberLoginRequest(email="fail@gmail.com", password="fail password", )

    # when & then
    with pytest.raises(ValueError, match="회원 정보가 존재하지 않습니다."): member_service.login(member_login_request)


@pytest.mark.django_db
def test_create_token():
    # given
    member_repository = MemberRepository()
    member_service = MemberService(member_repository=member_repository)
    dto = MemberCreateRequest(
        name="test name",
        email="test@gmail.com",
        password="test password",
        age=20,
    )

    member_repository.create_member(dto)
    member_login_request: MemberLoginRequest = MemberLoginRequest(email="test@gmail.com", password="test password", )

    # when
    member_service.login(member_login_request)

    # then
    assert JwtRefreshToken.objects.filter().count() == 1

@pytest.mark.django_db
def test_get_member():
    # given
    member_repository = MemberRepository()
    member_service = MemberService(member_repository=member_repository)
    dto = MemberCreateRequest(
        name="test name",
        email="test@gmail.com",
        password="test password",
        age=20,
    )
    member: Member = member_repository.create_member(dto)

    # when
    find_member = member_service.get_member(member.member_id)

    # then
    assert find_member is not None
    assert find_member.member_id == member.member_id

@pytest.mark.django_db
def test_update_member():
    # given
    member_repository = MemberRepository()
    member_service = MemberService(member_repository=member_repository)
    dto = MemberCreateRequest(
        name="test name",
        email="test@gmail.com",
        password="test password",
        age=20,
    )
    member: Member = member_repository.create_member(dto)

    member_update_request = MemberUpdateRequest(
        name="test update name",
        email="test_update@gmail.com",
        password="test update password",
        age=25,
    )

    # when
    member_service.update_member(member_id = member.member_id, dto = member_update_request)

    # then
    find_member = Member.objects.get(member_id=member.member_id)
    assert find_member is not None
    assert find_member.name == member_update_request.name
    assert find_member.email == member_update_request.email
    assert find_member.age == member_update_request.age

@pytest.mark.django_db
def test_delete_member():
    # given
    member_repository = MemberRepository()
    member_service = MemberService(member_repository=member_repository)
    dto = MemberCreateRequest(
        name="test name",
        email="test@gmail.com",
        password="test password",
        age=20,
    )
    member: Member = member_repository.create_member(dto)

    # when
    member_service.delete_member(member.member_id)

    # then
    assert Member.objects.filter().count() == 0