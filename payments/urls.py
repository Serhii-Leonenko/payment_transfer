from django.urls import path

from payments.views import TransferView

app_name = 'payments'

urlpatterns = [
    path("", TransferView.as_view(), name="transfer")
]