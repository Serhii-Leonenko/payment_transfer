from django.contrib.auth import get_user_model
from django.test import TestCase

from base.tests.factories import BankAccountFactory
from payments.models import BankAccount
from payments.services import (
    TransferService,
    InvalidAmountError,
    SameAccountError,
    NotEnoughMoneyError,
)
User = get_user_model()


class TransferServiceTests(TestCase):
    def setUp(self):
        self.account_from: BankAccount = BankAccountFactory(balance=1000)
        self.account_to: BankAccount = BankAccountFactory(balance=500)

    def test_transfer_success(self):
        TransferService.transfer(
            account_from=self.account_from,
            account_to=self.account_to,
            amount=300,
        )
        self.account_from.refresh_from_db()
        self.account_to.refresh_from_db()
        self.assertEqual(self.account_from.balance, 700)
        self.assertEqual(self.account_to.balance, 800)

    def test_transfer_invalid_amount_raises_error(self):
        for invalid_amount in [0, -100]:
            with self.subTest(invalid_amount=invalid_amount):
                with self.assertRaises(InvalidAmountError):
                    TransferService.transfer(
                        account_from=self.account_from,
                        account_to=self.account_to,
                        amount=invalid_amount,
                    )
                self.account_from.refresh_from_db()
                self.account_to.refresh_from_db()
                self.assertEqual(self.account_from.balance, 1000)
                self.assertEqual(self.account_to.balance, 500)

    def test_transfer_to_same_account_raises_error(self):
        with self.assertRaises(SameAccountError):
            TransferService.transfer(
                account_from=self.account_from,
                account_to=self.account_from,
                amount=100,
            )
        self.account_from.refresh_from_db()
        self.assertEqual(self.account_from.balance, 1000)

    def test_transfer_not_enough_money_raises_error(self):
        with self.assertRaises(NotEnoughMoneyError):
            TransferService.transfer(
                account_from=self.account_from,
                account_to=self.account_to,
                amount=1500,
            )
        self.account_from.refresh_from_db()
        self.account_to.refresh_from_db()
        self.assertEqual(self.account_from.balance, 1000)
        self.assertEqual(self.account_to.balance, 500)
