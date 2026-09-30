import logging

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from payments.forms import BankTransferForm
from payments.services import TransferService, InvalidAmountError, SameAccountError, NotEnoughMoneyError, \
    TransferServiceError

logger = logging.getLogger(__name__)


class TransferView(FormView):
    template_name = "payments/transfer.html"
    form_class = BankTransferForm
    success_url = reverse_lazy("payments:transfer")

    def form_valid(self, form):
        account_from = form.cleaned_data["account_from"]
        account_to = form.cleaned_data["account_to"]
        amount = form.cleaned_data["amount"]

        try:
            TransferService.transfer(
                account_from=account_from,
                account_to=account_to,
                amount=amount,
            )
            messages.success(self.request, "Transfer completed successfully.")

            return redirect(self.get_success_url())
        except InvalidAmountError:
            form.add_error("amount", "Amount must be greater than zero.")
        except SameAccountError as error:
            form.add_error("account_to", str(error))
        except NotEnoughMoneyError as error:
            form.add_error("amount", str(error))
        except TransferServiceError as error:
            logger.exception(error)
            form.add_error(None, "Transfer failed. Please try again later.")

        return self.form_invalid(form)
