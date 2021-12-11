from django.test import TestCase
from ..models import SpendingORM


class SpendingTest(TestCase):

    def setUp(self):
        SpendingORM.objects.create(
            amount=12300, currency='FT', description='Christmas')
        SpendingORM.objects.create(
            amount=200, currency='EUR', description='Christmas as well')

    def test_spending_created(self):
        spending_christmas_ft = SpendingORM.objects.get(
            description='Christmas')
        spending_christmas_eur = SpendingORM.objects.get(
            description='Christmas as well')
        self.assertEqual(
            spending_christmas_ft.amount, 12300)
        self.assertEqual(
            spending_christmas_eur.amount, 200)
