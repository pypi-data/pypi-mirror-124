from datetime import date
from random import choice, randint
from urllib.parse import urlparse

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.timezone import get_default_timezone, localdate

from django_ledger.models import EntityModel
from django_ledger.settings import DJANGO_LEDGER_LOGIN_URL
from django_ledger.tests.base import DjangoLedgerBaseTest
from django_ledger.urls.transactions import urlpatterns as transaction_urls
from django_ledger.utils import populate_default_coa, generate_sample_data

UserModel = get_user_model()


class EntityModelTests(DjangoLedgerBaseTest):

    def setUp(self) -> None:
        super(EntityModelTests, self).setUp()

        self.TRANSACTION_URLS = {
            p.name: set(p.pattern.converters.keys()) for p in transaction_urls
        }

