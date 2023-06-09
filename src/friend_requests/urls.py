from django.urls import path
from friend_requests.views import FriendRequestViewSet

urlpatterns = [
    path('', FriendRequestViewSet.as_view({'post': 'create'}), name='friend_request'),
    path('outcoming/', FriendRequestViewSet.as_view({'get': 'outcoming_requests'}), name='outcoming_requests'),
    path('incoming/', FriendRequestViewSet.as_view({'get': 'incoming_requests'}), name='incoming_requests'),
    path(
        '<int:pk>/approve/', FriendRequestViewSet.as_view({'post': 'approve'}),
        name='approve_request'
    ),
    path(
        '<int:pk>/decline/', FriendRequestViewSet.as_view({'post': 'decline'}),
        name='decline_request'
    )
]