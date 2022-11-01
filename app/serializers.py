from rest_framework import serializers

from . import models


class DonutSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Donut
        fields = ["id", "code", "description", "price_per_unit"]


class OrderSerializer(serializers.Serializer):
    donut_code = serializers.CharField()
    quantity = serializers.IntegerField(required=False)


class CreateOrderSerializer(serializers.Serializer):
    donuts = serializers.ListField(child=OrderSerializer())


class ListOrderSerializer(serializers.ModelSerializer):
    donut_code = serializers.SerializerMethodField()

    def get_donut_code(self, obj):
        return obj.donut_code.code

    class Meta:
        model = models.Order
        fields = "__all__"
