from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from base.tests.factories import BankAccountFactory
from payments.forms import BankTransferForm
from payments.models import BankAccount
from payments.services import TransferService, InvalidAmountError, SameAccountError, NotEnoughMoneyError


class TestTransferView(TestCase):
    def setUp(self):
        self.url = reverse("payments:transfer")
        self.account_from: BankAccount = BankAccountFactory(balance=10000)
        self.account_to: BankAccount = BankAccountFactory(balance=500)

    def test_renders_form(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "payments/transfer.html")
        self.assertIsInstance(response.context["form"], BankTransferForm)

    @patch.object(TransferService, "transfer")
    def test_transfer_success(self, mock_transfer):
        response = self.client.post(
            self.url,
            data={
                "amount": 10,
                "account_from": self.account_from.id,
                "account_to": self.account_to.id
            }
        )
        self.assertRedirects(response, self.url)
        mock_transfer.assert_called_once_with(
            account_from=self.account_from,
            account_to=self.account_to,
            amount=1000
        )

    @patch.object(TransferService, "transfer")
    def test_render_errors(self, mock_transfer):
        errors = [
            InvalidAmountError(),
            SameAccountError(),
            NotEnoughMoneyError(),
        ]

        for error in errors:
            with self.subTest(error=error):
                mock_transfer.side_effect = error
                response = self.client.post(
                    self.url,
                    data={
                        "amount": 10,
                        "account_from": self.account_from.id,
                        "account_to": self.account_to.id
                    }
                )
                self.assertEqual(response.status_code, 200)

                match error:
                    case InvalidAmountError():
                        self.assertFormError(response.context["form"], "amount", "Amount must be greater than zero.")
                    case SameAccountError():
                        self.assertFormError(response.context["form"], "account_to", "You cannot transfer to the same account.")
                    case NotEnoughMoneyError():
                        self.assertFormError(response.context["form"], "amount", "Not enough money.")
