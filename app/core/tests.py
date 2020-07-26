import datetime

from django.db import IntegrityError
from freezegun import freeze_time

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import User, Post
from user.serializers import UserLoginSerializer


USER_SIGNUP_URL = reverse("user:signup")
USER_SIGNIN_URL = reverse("user:signin")
USER_PROFILE_URL = reverse("user:profile")
USER_ANALITICS_URL = reverse("user:analitics")
POSTS_URL = reverse("post:posts-list")


def make_like_url(post_id: int) -> str:
    return f'{POSTS_URL}{post_id}/like/'


def sample_user(
        email: str = "test@testemail.com",
        password: str = "testpass",
        name: str = "testUser"
) -> dict:
    try:
        user = get_user_model().objects.create_user(email,
                                                    password=password,
                                                    name=name)
    except IntegrityError:
        user = User.objects.get(email=email)
    return {"user": user, "password": password}


def get_user_token(user: dict) -> dict:
    payload = {
        "email": user["user"].email,
        "password": user["password"],
        "name": user["user"].name
    }
    serializer = UserLoginSerializer(data=payload)
    serializer.is_valid(raise_exception=True)
    return {'token': serializer.data['token']}


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_with_email_successful(self):
        email = "test@testemail.com"
        password = "Testpass123"
        name = "testUser"

        create_user = self.client.post(USER_SIGNUP_URL, {"email": email,
                                                         "password": password,
                                                         "name": name})
        user = User.objects.get(email=email)

        self.assertEqual(create_user.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_email(self):
        user = self.client.post(
            USER_SIGNUP_URL,
            {"email": "wrong_email", "password": "password", "name": "name"}
        )
        is_user = User.objects.filter(email="wrong_email").exists()

        self.assertEqual(user.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(is_user, False)

    def test_user_get_token(self):
        user = sample_user()
        token = self.client.post(USER_SIGNIN_URL, {
            "email": user["user"].email,
            "password": user["password"],
            "name": user["user"].name
        })

        self.assertEqual(token.status_code, status.HTTP_200_OK)


class PostsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = sample_user()
        self.token = get_user_token(self.user)
        self.client.force_authenticate(self.user["user"],
                                       token=self.token['token'])

    def create_post(self, text: str = 'Some example text'):
        return self.client.post(POSTS_URL, {"text": text})

    def test_post_create_success(self):
        res = self.create_post()
        post = self.client.get(POSTS_URL)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, post.json()[0])

    def test_post_create_unauthorized(self):
        self.client.logout()
        res = self.create_post()
        post = Post.objects.count()

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(post, 0)

    def test_like_post_success_and_only_once(self):
        post = self.create_post()
        post_id = post.json()["id"]

        make_like = self.client.post(make_like_url(post_id))
        make_like_once_more = self.client.post(make_like_url(post_id))
        like = self.client.get(f'{POSTS_URL}{post_id}/')

        self.assertEqual(make_like.status_code, status.HTTP_200_OK)
        self.assertEqual(make_like_once_more.status_code, status.HTTP_200_OK)
        self.assertEqual(like.json()['likes_count'], 1)

    def test_delete_like_from_post_success(self):
        post = self.create_post()
        post_id = post.json()["id"]

        make_like = self.client.post(make_like_url(post_id))
        check_like = self.client.get(f'{POSTS_URL}{post_id}/')

        delete_like = self.client.delete(make_like_url(post_id))
        check_deleted_like = self.client.get(f'{POSTS_URL}{post_id}/')

        self.assertEqual(make_like.status_code, status.HTTP_200_OK)
        self.assertEqual(check_like.json()['likes_count'], 1)
        self.assertEqual(delete_like.status_code, status.HTTP_200_OK)
        self.assertEqual(check_deleted_like.json()['likes_count'], 0)

    def test_different_users_can_like_post(self):
        post = self.create_post()
        post_id = post.json()["id"]

        make_like = self.client.post(make_like_url(post_id))

        self.client.logout()
        self.user = sample_user(email='another_user@test.com',
                                password='testPassword',
                                name='AnotherUser')
        self.token = get_user_token(self.user)
        self.client.force_authenticate(self.user["user"],
                                       token=self.token['token'])

        make_another_like = self.client.post(make_like_url(post_id))

        like = self.client.get(f'{POSTS_URL}{post_id}/')

        self.assertEqual(make_like.status_code, status.HTTP_200_OK)
        self.assertEqual(make_another_like.status_code, status.HTTP_200_OK)
        self.assertEqual(like.json()['likes_count'], 2)

    def test_user_analitics(self):
        """
        Test likes filering by date.
        Creates 6 posts and every post likes with different date, then filters
        from the second one to the one before the last
        Result of filtering should be 4 likes
        """
        post_and_likes_count = 6
        filtered_likes_count = 4
        dates_list = [
            datetime.date.today() - datetime.timedelta(num)
            for num in range(post_and_likes_count)
        ]
        for date in dates_list:
            with freeze_time(date):
                post = self.create_post()
                post_id = post.json()["id"]
                self.client.post(make_like_url(post_id))

        res = self.client.get(
            f"{USER_ANALITICS_URL}?date_from={dates_list[-2]}"
            f"&date_to={dates_list[1]}"
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["likes"], filtered_likes_count)
