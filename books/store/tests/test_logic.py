from django.contrib.auth.models import User
from django.test import TestCase

from store.logic import set_rating
from store.models import Book, UserBookRelation


class SetRatingTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='test_user1',
                                         first_name='Ivan',
                                         last_name='Petrov')
        self.user2 = User.objects.create(username='test_user2',
                                         first_name='Dima',
                                         last_name='Shilov')
        self.user3 = User.objects.create(username='test_user3',
                                         first_name='Sergey',
                                         last_name='Smyshlyaev')
        self.book1 = Book.objects.create(name='Hotel',
                                         price=77.33,
                                         author_name='Arthur Haighley',
                                         owner=self.user1)

        UserBookRelation.objects.create(
            user=self.user1, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(
            user=self.user2, book=self.book1, like=True, rate=5)
        UserBookRelation.objects.create(
            user=self.user3, book=self.book1, like=True, rate=4)

    def test_set_rating(self):
        set_rating(self.book1)
        self.book1.refresh_from_db()
        self.assertEqual('4.67', str(self.book1.rating))

