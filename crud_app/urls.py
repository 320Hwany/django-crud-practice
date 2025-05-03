from django.urls import path

from crud_app.views import MemberView

urlpatterns = [
    path("members", MemberView.as_view(), name="member-view"),
]