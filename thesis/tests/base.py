from unittest import mock

from django.test import TestCase

from thesis.utils.address import AddressParser, ParsedAddress


class BaseTestCase(TestCase):
    def setUp(self) -> None:
        patcher = mock.patch.object(
            AddressParser, "from_string", return_value=ParsedAddress(x=53.53, y=53.53)
        )
        patcher.start()
