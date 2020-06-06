from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from core.models import Tag
from recipe.serializers import TagSerializer

TAG_URL = reverse('recipe:tag-list')

class PublicTagsApiTests(TestCase):
    ''' Test the public available Tag API '''
    def setUp(self):
        self.client = APIClient()

    def test_login_require(self):
        res = self.client.get(TAG_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'rg171195@gmail.com'
            'pass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrive_tags(self):
        Tags.objects.create(self.user, name='Vegan')
        Tags.objects.create(self.user, name='Dessert')
        res = self.client.get(TAG_URL)
        tags = Tags.object.all().orderby('-name')
        serializer =  TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tags_limited_to_user(self):
        """Test that tags returned are for authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@gmail.com',
            'testpass'
        )
        Tag.objects.create(user=user2, name='Fruity')
        tag = Tag.objects.create(user=self.user, name='Comfort Food')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)
