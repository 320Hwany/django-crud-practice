from django.urls import path

from crud_app.views import MemberView, MemberLoginView

urlpatterns = [
    path("members", MemberView.as_view(), name="member-view"),
    path("login", MemberLoginView.as_view(), name="login"),
]