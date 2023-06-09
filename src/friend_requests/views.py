from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from friend_requests.constants import FriendRequestStatus
from friend_requests.models import FriendRequest
from friend_requests.serializers import CreateFriendRequestSerializer, FriendRequestSerializer
from friend_requests.services import SendRequestService
from friend_requests.exception import FriendRequestAPIException
from rest_framework import status, response

from friend_requests.services.approve_request import ApproveRequestService
from friend_requests.services.decline_request import DeclineRequestService


class FriendRequestViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated, )
    serializer_class = FriendRequestSerializer
    queryset = FriendRequest.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateFriendRequestSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serivce = SendRequestService(
            from_user=self.request.user, to_user=serializer.validated_data['to_user']
        )
        res, msg, friend_request = serivce.run()
        if not res:
            raise FriendRequestAPIException(msg)
        return response.Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        if self.action in {'approve', 'decline'}:
            return self.queryset.filter(to_user=self.request.user)
        if self.action == 'outcoming_requests':
            return self.queryset.filter(from_user=self.request.user, status=FriendRequestStatus.new)
        if self.action == 'incoming_requests':
            return self.queryset.filter(to_user=self.request.user, status=FriendRequestStatus.new)
        return super().get_queryset()
    
    def approve(self, request, *args, **kwargs):
        instance = self.get_object()
        service = ApproveRequestService(request=instance)
        res, msg, friend_request = service.run()
        if not res:
            raise FriendRequestAPIException(msg) 
        return response.Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_200_OK)

    def decline(self, request, *args, **kwargs):
        instance = self.get_object()
        service = DeclineRequestService(request=instance)
        res, msg, friend_request = service.run()
        if not res:
            raise FriendRequestAPIException(msg) 
        return response.Response(FriendRequestSerializer(friend_request).data, status=status.HTTP_200_OK)

    def outcoming_requests(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def incoming_requests(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
