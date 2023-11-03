import factory
from .models import Poll

class PollFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Poll

    question = "Sample poll question"
    pub_date = factory.Faker('date_time', tzinfo=None)
    end_date = factory.Faker('date_time', tzinfo=None)