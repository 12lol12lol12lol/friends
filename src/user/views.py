from django.shortcuts import get_object_or_404
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.exceptions import UserAPIException
from user.models import User
from user.serializers import FriendSerializer, FriendShipStatusSerializer, RegisterUserSerializer
from rest_framework import response, status
from user.services.delete_from_friends import DeleteFromFriendsService

from user.services.friendship_status import FriendshipStatusService


class RegisterUserView(CreateAPIView):
    permission_classes = (AllowAny, )
    serializer_class = RegisterUserSerializer


class FriendListView(ListAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = FriendSerializer

    def get_queryset(self):
        return self.request.user.friends.all()


class FriendshipStatusView(APIView):
    """
    View for friendship status
    """
    permission_classes = (IsAuthenticated, )
    serializer_class = FriendShipStatusSerializer

    def get(self, request, pk, **kwargs):
        """
        Return friendship status.
        """
        user = get_object_or_404(User, pk=pk)
        service = FriendshipStatusService(from_user=self.request.user, to_user=user)
        res, msg, friendship_status = service.run()
        if not res:
            raise UserAPIException(msg)
        return response.Response(
            {
                'id': user.id,
                'status': friendship_status,
            },
            status=status.HTTP_200_OK
        )

class DeleteFromFriendsView(APIView):
    """
    View for delete user from friends
    """
    permission_classes = (IsAuthenticated, )

    def delete(self, request, pk, **kwargs):
        """
        Delete user from frinds.
        """
        user = get_object_or_404(User, pk=pk)
        service = DeleteFromFriendsService(from_user=self.request.user, to_user=user)
        res, msg, _ = service.run()
        if not res:
            raise UserAPIException(msg)
        return response.Response(status=status.HTTP_204_NO_CONTENT)