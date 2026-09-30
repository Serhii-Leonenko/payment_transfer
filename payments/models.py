from django.conf import settings
from django.db import models


class BankAccount(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    balance = models.PositiveIntegerField(
        default=0
    )

    def __str__(self):
        return f"{self.user.username}: balance: {self.balance / 100}"
