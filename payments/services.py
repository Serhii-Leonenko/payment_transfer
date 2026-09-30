from django.db import transaction
from django.db.models import F

from payments.models import BankAccount


class TransferServiceError(Exception):
    pass


class InvalidAmountError(TransferServiceError):
    pass


class SameAccountError(TransferServiceError):
    pass


class NotEnoughMoneyError(TransferServiceError):
    pass



class TransferService:
    @classmethod
    def transfer(
        cls,
        account_from: BankAccount,
        account_to: BankAccount,
        amount: int,
    ) -> None:
        if amount <= 0:
            raise InvalidAmountError(
                f"account_from: {amount} balance: {account_from.balance}. "
                f"Amount is lover than or equal to zero."
            )

        if account_from.pk == account_to.pk:
            raise SameAccountError("You can't transfer to the same account.")

        if account_from.balance < amount:
            raise NotEnoughMoneyError("Not enough money.")

        with transaction.atomic():
            BankAccount.objects.filter(
                pk=account_from.pk,
            ).update(
                balance=F("balance") - amount
            )

            BankAccount.objects.filter(
                pk=account_to.pk,
            ).update(
                balance=F("balance") + amount
            )
