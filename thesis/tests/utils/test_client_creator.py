from thesis.models import Client
from thesis.tests.base import BaseTestCase
from thesis.utils.client_creator import ClientCreator, parse_utm_labels_from_url


class ClientCreatorTestCase(BaseTestCase):
    def test_process_website_source(self):
        params = {"name": "Me", "utm_content": "ABC", "source": Client.Source.WEB_SITE}

        result = ClientCreator().process(**params)

        self.assertIsNotNone(result)
        self.assertEqual(1, Client.objects.filter(id=result.id).count())
        self.assertEqual("Me", Client.objects.get(id=result.id).name)
        self.assertEqual(Client.Source.WEB_SITE, Client.objects.get(id=result.id).source)

    def test_process_call_center_source(self):
        params = {
            "name": "Me",
            "utm_content": "ABC",
            "source": Client.Source.CALL_CENTER,
        }

        result = ClientCreator().process(**params)

        self.assertIsNotNone(result)
        self.assertEqual(1, Client.objects.filter(id=result.id).count())
        self.assertEqual("Me", Client.objects.get(id=result.id).name)
        self.assertEqual(Client.Source.CALL_CENTER, Client.objects.get(id=result.id).source)

    def test_parse_utm_labels_from_url_no_query_params(self):
        example_url = "https://domain.ru/"
        result = parse_utm_labels_from_url(example_url)

        self.assertIsNone(result.utm_source)
        self.assertIsNone(result.utm_campaign)
        self.assertIsNone(result.utm_content)
        self.assertIsNone(result.utm_medium)
        self.assertIsNone(result.utm_term)

    def test_parse_utm_labels_from_url_single_utm(self):
        example_url = "https://domain.ru/?utm_source=abc"
        result = parse_utm_labels_from_url(example_url)

        self.assertEqual("abc", result.utm_source)
        self.assertIsNone(result.utm_campaign)
        self.assertIsNone(result.utm_content)
        self.assertIsNone(result.utm_medium)
        self.assertIsNone(result.utm_term)

    def test_parse_utm_labels_from_url_several_values(self):
        example_url = "https://domain.ru/?utm_source=abc&utm_source=agfds"
        result = parse_utm_labels_from_url(example_url)

        # the first one is taken
        self.assertEqual("abc", result.utm_source)
        self.assertIsNone(result.utm_campaign)
        self.assertIsNone(result.utm_content)
        self.assertIsNone(result.utm_medium)
        self.assertIsNone(result.utm_term)
