from django.urls import path
from user.views import FriendListView, FriendshipStatusView, RegisterUserView, DeleteFromFriendsView

urlpatterns = [
    path('friends/', FriendListView.as_view(), name='friend_list'),
    path('<int:pk>/', DeleteFromFriendsView.as_view(), name='delete_from_friends'),
    path('<int:pk>/friendship_status/', FriendshipStatusView.as_view(), name='friendship_status'),
    path('sign_up/', RegisterUserView.as_view(), name='register_user'),
]
