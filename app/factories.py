from factory.django import DjangoModelFactory
import factory
from factory import fuzzy
from . import models
from . import enums


class Donut(DjangoModelFactory):
    class Meta:
        model = models.Donut

    code = factory.Sequence(lambda n: "Code %03d" % n)
    description = factory.Sequence(lambda n: "Donut %03d" % n)
    price_per_unit = fuzzy.FuzzyFloat(0.5)


class Order(DjangoModelFactory):
    class Meta:
        model = models.Order

    donut_code = factory.SubFactory(Donut)
    state = enums.OrderStatus.CREATED.value
