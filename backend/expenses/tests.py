import datetime
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Expense


class ExpenseCRUDTests(APITestCase):

    def setUp(self):
        self.expense = Expense.objects.create(
            title="Bus ticket",
            amount=50.00,
            category="Transport",
            date=datetime.date.today(),
            payment_method="Cash",
            description="Daily commute"
        )
        self.list_url = reverse('expense-list')
        self.detail_url = reverse('expense-detail', args=[self.expense.id])

    def test_create_expense_success(self):
        payload = {
            "title": "Lunch",
            "amount": 120.50,
            "category": "Food",
            "date": str(datetime.date.today()),
            "payment_method": "UPI",
            "description": "Canteen lunch"
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 2)

    def test_create_expense_invalid_amount(self):
        payload = {
            "title": "Bad expense",
            "amount": -10,
            "category": "Food",
            "date": str(datetime.date.today()),
            "payment_method": "Cash",
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_expense_missing_title(self):
        payload = {
            "amount": 20,
            "category": "Food",
            "date": str(datetime.date.today()),
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_expenses(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_expense(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Bus ticket")

    def test_update_expense_put(self):
        payload = {
            "title": "Bus ticket updated",
            "amount": 60.00,
            "category": "Transport",
            "date": str(datetime.date.today()),
            "payment_method": "Card",
            "description": "Updated"
        }
        response = self.client.put(self.detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.amount, 60.00)

    def test_partial_update_expense_patch(self):
        response = self.client.patch(self.detail_url, {"amount": 75.00}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expense.refresh_from_db()
        self.assertEqual(float(self.expense.amount), 75.00)

    def test_delete_expense(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Expense.objects.count(), 0)

    def test_filter_by_category(self):
        Expense.objects.create(
            title="Groceries", amount=300, category="Food",
            date=datetime.date.today(), payment_method="Cash"
        )
        response = self.client.get(self.list_url, {"category": "Food"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_by_date(self):
        response = self.client.get(self.list_url, {"date": str(datetime.date.today())})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_future_date_rejected(self):
        future_date = datetime.date.today() + datetime.timedelta(days=5)
        payload = {
            "title": "Future expense",
            "amount": 10,
            "category": "Other",
            "date": str(future_date),
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_category_rejected(self):
        payload = {
            "title": "Weird category",
            "amount": 10,
            "category": "NotACategory",
            "date": str(datetime.date.today()),
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_nonexistent_expense_404(self):
        response = self.client.get(reverse('expense-detail', args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
