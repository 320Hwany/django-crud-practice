from django.db import models



class Member(models.Model):
    member_id: models.BigAutoField = models.BigAutoField(primary_key=True)
    name: models.CharField = models.CharField(max_length=100)
    email: models.EmailField = models.EmailField()
    password: models.CharField = models.CharField(max_length=100)
    age: models.IntegerField = models.IntegerField()

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'members'


class Order(models.Model):
    order_id: models.BigAutoField = models.BigAutoField(primary_key=True)
    member_id: models.BigIntegerField = models.BigIntegerField()
    price: models.IntegerField = models.IntegerField()

    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'


class JwtRefreshToken(models.Model):
    jwt_refresh_token_id: models.BigAutoField = models.BigAutoField(primary_key=True)
    member_id: models.BigIntegerField = models.BigIntegerField()
    refresh_token: models.CharField = models.CharField(max_length=500)
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'jwt_refresh_token'

