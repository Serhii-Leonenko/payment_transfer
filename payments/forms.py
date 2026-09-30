from django import forms

from payments.models import BankAccount


class BankTransferForm(forms.Form):
    account_from = forms.ModelChoiceField(
        queryset=BankAccount.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    account_to = forms.ModelChoiceField(
        queryset=BankAccount.objects.all(),
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0.01,
        widget=forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
    )

    def clean_account_to(self) -> BankAccount:
        if self.cleaned_data['account_from'] == self.cleaned_data['account_to']:
            raise forms.ValidationError("You can't transfer to the same account.")

        return self.cleaned_data['account_to']

    def clean_amount(self) -> int:
        amount = self.cleaned_data['amount']

        return amount * 100
