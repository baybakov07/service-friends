
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from oauth.views import UserCreateView, SendFriendRequestView, AcceptFriendRequestView, RejectFriendRequestView, \
    ListSendFriendRequestView, ListReceiveFriendRequestView, FriendshipStatusView, DeleteFriendView, ListFriendsView

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user-create'),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('friend_request/send/<int:to_user_id>/', SendFriendRequestView.as_view()),
    path('friend_requests/send/', ListSendFriendRequestView.as_view()),
    path('friend_requests/receive/', ListReceiveFriendRequestView.as_view()),
    path('friend_request/accept/<int:from_user_id>/', AcceptFriendRequestView.as_view()),
    path('friend_request/reject/<int:from_user_id>/', RejectFriendRequestView.as_view()),
    path('friend_status/<int:other_user_id>/', FriendshipStatusView.as_view()),
    path('friends/delete/<int:other_user_id>/', DeleteFriendView.as_view()),
    path('friends/', ListFriendsView.as_view()),
]