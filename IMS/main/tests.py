
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Item

class InventoryItemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_create_item_success(self):
        data = {'name': 'Test Item', 'description': 'Test Description', 'quantity': 10}
        response = self.client.post('/items/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(Item.objects.get().name, 'Test Item')

    def test_create_item_failure_duplicate(self):
        Item.objects.create(name='Test Item', description='Test Description', quantity=10, owner=self.user)
        data = {'name': 'Test Item', 'description': 'New Description', 'quantity': 20}
        response = self.client.post('/items/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Item.objects.count(), 1)

    def test_retrieve_item_success(self):
        item = Item.objects.create(name='Test Item', description='Test Description', quantity=10, owner=self.user)
        response = self.client.get(f'/items/{item.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Item')

    def test_retrieve_item_failure(self):
        response = self.client.get('/items/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_item_success(self):
        item = Item.objects.create(name='Test Item', description='Test Description', quantity=10, owner=self.user)
        data = {'name': 'Updated Item', 'description': 'Updated Description', 'quantity': 20}
        response = self.client.put(f'/items/{item.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Item')
        self.assertEqual(response.data['description'], 'Updated Description')
        self.assertEqual(response.data['quantity'], 20)

    def test_update_item_failure(self):
        response = self.client.put('/items/999/', {'name': 'Updated Item'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_item_success(self):
        item = Item.objects.create(name='Test Item', description='Test Description', quantity=10, owner=self.user)
        response = self.client.delete(f'/items/{item.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)

    def test_delete_item_failure(self):
        response = self.client.delete('/items/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)