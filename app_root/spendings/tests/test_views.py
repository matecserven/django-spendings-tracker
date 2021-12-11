from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from spendings.models import SpendingORM
from spendings.serializers import SpendingSerializer


class SpendingsTests(APITestCase):
    url_list = reverse('spendingorm-list')

    def setUp(self):
        self.forint_spending = SpendingORM.objects.create(
            amount=12300, currency='FT', description='Christmas')
        self.euro_spending = SpendingORM.objects.create(
            amount=200, currency='EUR', description='Christmas as well')

    def test_get_all_spending(self):
        response = self.client.get(self.url_list)
        spendings = SpendingORM.objects.all()
        serializer = SpendingSerializer(spendings, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_spending(self):
        url = reverse('spendingorm-detail', kwargs={
            'pk': self.forint_spending.id})
        response = self.client.get(url)
        single_spending = SpendingORM.objects.get(pk=self.forint_spending.id)
        serializer = SpendingSerializer(single_spending)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_spending(self):
        url = reverse('spendingorm-detail', kwargs={'pk': 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_spendings_filtered_by_currency(self):
        response = self.client.get(self.url_list, {'currency': 'FT'})
        serializer = SpendingSerializer(self.forint_spending)
        self.assertEqual(response.data, [serializer.data])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_spendings_filtered_by_not_existing_currency(self):
        response = self.client.get(self.url_list, {'currency': 'USD'})
        self.assertEqual(len(response.data), 0)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_spendings_ordered_ascending(self):
        response = self.client.get(self.url_list, {'order': 'asc'})
        ascending_spendings = SpendingORM.objects.all().order_by('amount')
        serializer = SpendingSerializer(ascending_spendings, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_spendings_ordered_descending(self):
        response = self.client.get(self.url_list, {'order': 'desc'})
        descending_spendings = SpendingORM.objects.all().order_by('amount').reverse()
        serializer = SpendingSerializer(descending_spendings, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_valid_spending(self):
        data = {'amount': 123, 'currency': 'FT', 'description': 'Christmas'}
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SpendingORM.objects.count(), 3)

    def test_create_invalid_spending(self):
        data = {
            'amount': 123,
            'currency': 'Forint',
            'description': 'Christmas'
        }
        response = self.client.post(self.url_list, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(SpendingORM.objects.count(), 2)

    def test_valid_update_forint_spending(self):
        url = reverse('spendingorm-detail', kwargs={
            'pk': self.forint_spending.id})
        data = {
            'amount': 22000,
            'currency': 'FT',
            'description': 'Christmas'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        single_spending = SpendingORM.objects.get(pk=self.forint_spending.id)
        serializer = SpendingSerializer(single_spending)
        self.assertEqual(response.data, serializer.data)

    def test_invalid_update_forint_spending(self):
        url = reverse('spendingorm-detail', kwargs={
            'pk': self.forint_spending.id})
        data = {
            'amount': -1500,
            'currency': 'FT',
            'description': 'Christmas'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_forint_spending(self):
        url = reverse('spendingorm-detail', kwargs={
            'pk': self.forint_spending.id})
        response = self.client.delete(url)
        spendings = SpendingORM.objects.all()
        serilizer = SpendingSerializer(spendings, many=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(serilizer.data), 1)

    def test_delete_non_existing_spending(self):
        url = reverse('spendingorm-detail', kwargs={
            'pk': 999})
        response = self.client.delete(url)
        spendings = SpendingORM.objects.all()
        serilizer = SpendingSerializer(spendings, many=True)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(len(serilizer.data), 2)
