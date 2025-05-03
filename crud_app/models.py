from django.db import models

from crud_app.dtos.dtos import MemberCreateRequest
from crud_app.entities.entities import OrderEntity


class Member(models.Model):
    member_id: models.BigAutoField = models.BigAutoField(primary_key=True)
    name: models.CharField = models.CharField(max_length=100)
    email: models.EmailField = models.EmailField()
    age: models.IntegerField = models.IntegerField()

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'members'

    @classmethod
    def from_create_request(cls, dto: MemberCreateRequest) -> 'Member':
        return cls(
            name=dto.name,
            email=dto.email,
            age=dto.age,
        )


class Order(models.Model):
    order_id: models.BigAutoField = models.BigAutoField(primary_key=True)
    member_id: models.BigIntegerField = models.BigIntegerField()
    price: models.IntegerField = models.IntegerField()

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'

    @classmethod
    def from_entity(cls, entity: OrderEntity) -> 'Order':
        return cls(
            order_id=entity.order_id,
            member_id=entity.member_id,
            price=entity.price,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
