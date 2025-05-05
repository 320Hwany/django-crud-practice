from django.urls import path

from crud_app.views import MemberView, MemberListView, MemberLoginView

urlpatterns = [
    path("members", MemberView.as_view(), name="member-view"),
    path("members/<int:member_id>", MemberListView.as_view(), name="member-detail-view"),
    path("login", MemberLoginView.as_view(), name="login"),
]