import uuid

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from . import publish

from . import enums


class Donut(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(unique=True, max_length=30)
    description = models.CharField(max_length=30)
    price_per_unit = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=Donut)
def donut_created(sender, instance, **kwargs):
    publish.publish_message(enums.Channel.DONUT.value, instance.code)


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    donut_code = models.ForeignKey(
        Donut, related_name="orders", on_delete=models.PROTECT
    )
    state = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def new(
        cls,
        *,
        donut_code,
        state,
    ):
        return cls.objects.create(
            donut_code=donut_code,
            state=state,
        )


@receiver(post_save, sender=Order)
def order_created(sender, instance, **kwargs):
    publish.publish_message(enums.Channel.ORDER.value, str(instance.id))
