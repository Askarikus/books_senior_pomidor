from django.contrib.auth.models import User
from django.db.models import Count, Case, When, Avg
from django.test import TestCase

from store.models import Book, UserBookRelation
from store.serializers import BooksSerializer


class BooksSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(username='test_user1')
        self.user2 = User.objects.create(username='test_user2')
        self.user3 = User.objects.create(username='test_user3')
        self.book1 = Book.objects.create(name='Hotel',
                                         price=77.33,
                                         author_name='Arthur Haighley',
                                         )
        self.book2 = Book.objects.create(name='Airport',
                                         price=88.50,
                                         author_name='Arthur Haighley',
                                         )
        self.books = Book.objects.all().annotate(annotated_likes=Count(
                Case(
                    When(
                        book__like=True,  # related_name in UserBookRelation, field book
                        then=1
                    )
                )
            ),
            rating=Avg('book__rate')
        ).order_by('id')
        UserBookRelation.objects.create(
            user=self.user1, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(
            user=self.user2, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(
            user=self.user3, book=self.book1, like=True, rate=4)
        UserBookRelation.objects.create(
            user=self.user1, book=self.book2, like=True, rate=3)
        UserBookRelation.objects.create(
            user=self.user2, book=self.book2, like=False, rate=4)
        UserBookRelation.objects.create(
            user=self.user3, book=self.book2, like=True, )

    def test_serializer_ok(self):
        data = BooksSerializer(self.books, many=True).data
        expected_data = [
            {
                'id': self.book1.id,
                'name': 'Hotel',
                'price': '77.33',
                'author_name': 'Arthur Haighley',
                'likes_count': 3,
                'annotated_likes': 3,
                'rating': '4.67',

             },
            {
                'id': self.book2.id,
                'name': 'Airport',
                'price': '88.50',
                'author_name': 'Arthur Haighley',
                'likes_count': 2,
                'annotated_likes': 2,
                'rating': '3.50',
            }
        ]
        self.assertEqual(expected_data, data)


