from django.test import TestCase

from store.models import Book
from store.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):
    def test_serializer_ok(self):
        book1 = Book.objects.create(name='Hotel', price=77.33)
        book2 = Book.objects.create(name='Airport', price=88.50)
        data = BooksSerializer([book1, book2], many=True).data
        expected_data = [
            {
                'id': book1.id,
                'name': 'Hotel',
                'price': '77.33'
             },
            {
                'id': book2.id,
                'name': 'Airport',
                'price': '88.50'
            }
        ]
        self.assertEqual(expected_data, data)


