from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from friend_requests.services.common import add_to_friends, is_already_friends
from friend_requests.services.constants import DECLINED_MESSAGE
from tests.factory import TestFactory
from tests.utils import get_test_user_password, get_test_username
from user.constants import FriendshipStatus
from user.services.delete_from_friends import DELETE_YOURSELF_FROM_FRIENDS_MESSAGE, YOU_ARE_NOT_FRIENDS_MESSAGE
from user.services.friendship_status import WRONG_FRIENDSHIP_REQUEST_MESSAGE


class UserTests(APITestCase):

    def setUp(self) -> None:
        self.factory = TestFactory()
        return super().setUp()

    def test_user_sign_up_success(self):
        url = reverse('register_user')
        pswd = get_test_user_password()
        data = {
            'username': get_test_username(),
            'password': pswd,
            'password2': pswd,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_user_sign_up_diff_password(self):
        url = reverse('register_user')
        pswd = get_test_user_password()
        data = {
            'username': get_test_username(),
            'password': pswd,
            'password2': f'{pswd}1',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_sign_up_already_exist(self):
        url = reverse('register_user')
        username = get_test_username()
        pswd = get_test_user_password()
        data = {
            'username': username,
            'password': pswd,
            'password2': pswd,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        new_password = get_test_user_password()
        data = {
            'username': username,
            'password': new_password  
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_friend_list(self):
        # Initialize
        user1 = self.factory.create_user()
        user2 = self.factory.create_user()
        user3 = self.factory.create_user()
        add_to_friends(user1, user2)
        add_to_friends(user1, user3)
        url = reverse('friend_list')

        self.client.force_authenticate(user1)
        response = self.client.get(url)
        response_count = response.json()['count']
        result_list = [data['id'] for data in response.json()['results']]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_count, 2)
        self.assertListEqual(result_list, [user2.id, user3.id])

    def test_friendship_status_nothing(self):
        # Initialize
        user1 = self.factory.create_user()
        user2 = self.factory.create_user()
        url = reverse('friendship_status', kwargs={'pk': user2.id})
        expected_data = {
            'id': user2.id,
            'status': FriendshipStatus.nothing,
        }

        # Body
        self.client.force_authenticate(user1)
        response = self.client.get(url)
        response_data = response.json()

        # Check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, expected_data)

    def test_friendship_status_wrong_status(self):
        # Initialize
        user1 = self.factory.create_user()
        url = reverse('friendship_status', kwargs={'pk': user1.id})

        # Body
        self.client.force_authenticate(user1)
        response = self.client.get(url)
        response_data = response.json()['detail']

        # Check
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, WRONG_FRIENDSHIP_REQUEST_MESSAGE)

    def test_friendship_status_outcoming_request(self):
        # Initialize
        request = self.factory.create_request()
        user1 = request.from_user
        user2 = request.to_user
        url = reverse('friendship_status', kwargs={'pk': user2.id})
        expected_data = {
            'id': user2.id,
            'status': FriendshipStatus.outcoming_request,
        }

        # Body
        self.client.force_authenticate(user1)
        response = self.client.get(url)
        response_data = response.json()

        # Check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, expected_data)

    def test_friendship_status_incoming_request(self):
        # Initialize
        request = self.factory.create_request()
        user1 = request.to_user
        user2 = request.from_user
        url = reverse('friendship_status', kwargs={'pk': user2.id})
        expected_data = {
            'id': user2.id,
            'status': FriendshipStatus.incoming_request,
        }

        # Body
        self.client.force_authenticate(user1)
        response = self.client.get(url)
        response_data = response.json()

        # Check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, expected_data)

    def test_friendship_status_already_frinds(self):
        # Initialize
        user1 = self.factory.create_user()
        user2 = self.factory.create_user()
        add_to_friends(user1, user2)

        url = reverse('friendship_status', kwargs={'pk': user2.id})
        expected_data = {
            'id': user2.id,
            'status': FriendshipStatus.already_friends,
        }

        # Body
        self.client.force_authenticate(user1)
        response = self.client.get(url)
        response_data = response.json()

        # Check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data, expected_data)

    def test_delete_from_friends_yourself(self):
        # Initialize
        user1 = self.factory.create_user()
        url = reverse('delete_from_friends', kwargs={'pk': user1.pk})

        # Body
        self.client.force_authenticate(user1)
        response = self.client.delete(url)
        response_data = response.json()['detail']

        # Check
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, DELETE_YOURSELF_FROM_FRIENDS_MESSAGE)

    def test_delete_from_friends_not_friend(self):
        # Initialize
        user1 = self.factory.create_user()
        user2 = self.factory.create_user()
        url = reverse('delete_from_friends', kwargs={'pk': user2.pk})

        # Body
        self.client.force_authenticate(user1)
        response = self.client.delete(url)
        response_data = response.json()['detail']

        # Check
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, YOU_ARE_NOT_FRIENDS_MESSAGE)

    def test_delete_from_friends_success(self):
        # Initialize
        user1 = self.factory.create_user()
        user2 = self.factory.create_user()
        add_to_friends(user1, user2)
        url = reverse('delete_from_friends', kwargs={'pk': user2.pk})

        # Body
        self.client.force_authenticate(user1)
        response = self.client.delete(url)

        # Check
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(is_already_friends(user1, user2))

    def test_try_send_request_after_delete_from_friends(self):
        """
        если пользователь1 удаляет из друзей пользователя2,
        то их "дружба" автоматом прекращается, и пользователь2 не может
        больше отправлять заявки в друзья пользователю1, и пользователь1
        автоматически удаляется из друзей пользователя2
        """
        # Initialize
        user1 = self.factory.create_user()
        user2 = self.factory.create_user()
        add_to_friends(user1, user2)
        url = reverse('delete_from_friends', kwargs={'pk': user2.pk}) 
        self.client.force_authenticate(user1)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        url = reverse('friend_request')
        self.client.force_authenticate(user2)
        response = self.client.post(url, {
            'to_user': user1.id
        })
        response_data = response.json()['detail']
        
        # Check
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, DECLINED_MESSAGE)