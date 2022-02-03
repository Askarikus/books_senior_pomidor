from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from store.models import Book
from store.serializers import BooksSerializer


class BookApiTestCase(APITestCase):
    def test_get(self):
        book1 = Book.objects.create(name='Hotel', price=77.33)
        book2 = Book.objects.create(name='Airport', price=88.50)
        url = reverse('book-list')
        response = self.client.get(url)
        serializer_data = BooksSerializer([book1, book2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)
