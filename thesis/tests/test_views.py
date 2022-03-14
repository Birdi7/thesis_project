from django.test import Client as TestClient

from thesis.models import Client, Order
from thesis.tests.base import BaseTestCase


class CreateOrderViewTestCase(BaseTestCase):
    def setUp(self) -> None:
        self.client = TestClient()

    def test_ok(self):
        response = self.client.post("/order/", HTTP_REFERER="http://domain.ru/")
        self.assertEqual(200, response.status_code)
        self.assertTrue(Client.objects.exists())
        self.assertTrue(Order.objects.exists())

    def test_with_utm_labels(self):
        response = self.client.post("/order/", HTTP_REFERER="http://domain.ru/?utm_source=abc")
        self.assertEqual(200, response.status_code)
        self.assertTrue(Client.objects.exists())
        client = Client.objects.first()
        self.assertEqual("abc", client.utm_source)
