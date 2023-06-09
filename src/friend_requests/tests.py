from urllib import request

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from friend_requests.constants import FriendRequestStatus
from friend_requests.services.constants import (
    ALREADY_FRIENDS_MESSAGE, DECLINED_MESSAGE, REQUEST_TO_YOURSELF_MESSAGE, WRONG_REQUEST_STATUS_MESSAGE,
)
from friend_requests.services.send_request import is_already_friends
from tests.factory import TestFactory


class FriendsTests(APITestCase):
    def setUp(self) -> None:
        self.factory = TestFactory()
        return super().setUp()

    def test_send_request(self):
        # Initialize
        user1 = self.factory.create_user()
        user2 = self.factory.create_user()
        url = reverse('friend_request')

        expected_data = {
            'from_user': user1.id,
            'to_user': user2.id,
            'status': FriendRequestStatus.new,
        }

        # Body
        self.client.force_authenticate(user1)
        response = self.client.post(url, {'to_user': user2.id})
        response_data = response.json()
        # Check
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        del response_data['id']
        self.assertDictEqual(response_data, expected_data)
    
    def test_send_request_to_yourself(self):
        user1 = self.factory.create_user()
        url = reverse('friend_request')

        # Body
        self.client.force_authenticate(user1)
        response = self.client.post(url, {'to_user': user1.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['detail'], REQUEST_TO_YOURSELF_MESSAGE)
    
    def test_already_friends(self):
        # Intitialize
        user1 = self.factory.create_user()
        user2 = self.factory.create_user()
        url = reverse('friend_request')
        user1.friends.add(user2)
        
        # Body
        self.client.force_authenticate(user1)
        response = self.client.post(url, {'to_user': user2.id})
        response_data = response.json()
        # Check
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data.get('detail'), ALREADY_FRIENDS_MESSAGE)
    
    def test_mutual_requests(self):
        # Initialize
        user1 = self.factory.create_user()
        user2 = self.factory.create_user()
        url = reverse('friend_request')

        self.client.force_authenticate(user1)
        response = self.client.post(url, {'to_user': user2.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_data = {
            'from_user': user2.id,
            'to_user': user1.id,
            'status': FriendRequestStatus.auto_approved,
        }

        # Body
        self.client.force_authenticate(user2)
        response = self.client.post(url, {'to_user': user1.id})
        response_data = response.json()
        # Check
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        del response_data['id']
        self.assertEqual(response_data, expected_data)
        self.assertTrue(is_already_friends(user1, user2))

    def test_approve_request_successfull(self):
        # Initialize
        request = self.factory.create_request()
        user = request.to_user
        url = reverse('approve_request', kwargs={'pk': request.pk})

        # Body
        self.client.force_authenticate(user)
        response = self.client.post(url)

        # Check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(is_already_friends(user, request.from_user))
    
    def test_approve_declined_request(self):
        # Initialize
        request = self.factory.create_request(status=FriendRequestStatus.declined)
        user = request.to_user
        url = reverse('approve_request', kwargs={'pk': request.pk})

        # Body
        self.client.force_authenticate(user)
        response = self.client.post(url)
        response_data = response.json()

        # Check
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response_data['detail'], WRONG_REQUEST_STATUS_MESSAGE)

    def test_approve_another_request(self):
         # Initialize
        request = self.factory.create_request()
        user = request.from_user
        url = reverse('approve_request', kwargs={'pk': request.pk})

        # Body
        self.client.force_authenticate(user)
        response = self.client.post(url)

        # Check
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_decline_requst_successfull(self):
        # Initialize
        request = self.factory.create_request()
        user = request.to_user
        url = reverse('decline_request', kwargs={'pk': request.pk})

        # Body
        self.client.force_authenticate(user)
        response = self.client.post(url)

        # Check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(is_already_friends(user, request.from_user))

    def test_decline_another_request(self):
         # Initialize
        request = self.factory.create_request()
        user = request.from_user
        url = reverse('decline_request', kwargs={'pk': request.pk})

        # Body
        self.client.force_authenticate(user)
        response = self.client.post(url)

        # Check
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_outcoming_requests_success(self):
        # Initializer
        request = self.factory.create_request()
        _ = self.factory.create_request(to_user=request.from_user)
        user = request.from_user
        url = reverse('outcoming_requests')

        # Body
        self.client.force_authenticate(user)
        response = self.client.get(url)
        response_data = response.json()

        # Check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['count'], 1)
        self.assertEqual(response_data['results'][0]['id'], request.id)

    def test_incoming_requests_success(self):
        # Initializer
        request = self.factory.create_request()
        _ = self.factory.create_request(from_user=request.to_user)
        user = request.to_user
        url = reverse('incoming_requests')

        # Body
        self.client.force_authenticate(user)
        response = self.client.get(url)
        response_data = response.json()

        # Check
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['count'], 1)
        self.assertEqual(response_data['results'][0]['id'], request.id)
    

    def test_send_requst_after_declined(self):
        """
        если пользователь1 отклоняет заявку в друзья от пользователя2,
        то пользователь2 не может больше отправлять заявки в друзья пользователю1
        """
        user1 = self.factory.create_user()
        user2 = self.factory.create_user()

        # Make request
        make_request_url = reverse('friend_request')
        self.client.force_authenticate(user1)
        response = self.client.post(make_request_url, {
            'to_user': user2.id
        })
        request_id = response.json()['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Decline request
        decline_url = reverse('decline_request', kwargs={'pk': request_id})
        self.client.force_authenticate(user2)
        response = self.client.post(decline_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Try to send new request
        self.client.force_authenticate(user1)
        response = self.client.post(make_request_url, {
            'to_user': user2.id
        })
        response_data = response.json()['detail']
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data, DECLINED_MESSAGE)

    def test_mutual_requests_through_api(self):
        """
        если пользователь1 отправляет заявку в друзья пользователю2,
        а пользователь2 отправляет заявку пользователю1, то они автоматом
        становятся друзьями, их заявки автоматом принимаются 
        """
        user1 = self.factory.create_user()
        user2 = self.factory.create_user()
        url = reverse('friend_request')

        # User1 send to User2
        self.client.force_authenticate(user1)
        response = self.client.post(
            url,
            {
                'to_user': user2.id
            }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # User2 send to User1
        self.client.force_authenticate(user2)
        response = self.client.post(
            url,
            {
                'to_user': user1.id
            }
        )
        response_data = response.json()['status']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data, FriendRequestStatus.auto_approved)
        self.assertTrue(is_already_friends(user1, user2))
        

