import factory
from django.contrib.auth import get_user_model


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Faker("user_name")
    password = factory.django.Password('pw')


class BankAccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "payments.BankAccount"

    user = factory.SubFactory(UserFactory)
    balance = 100000
