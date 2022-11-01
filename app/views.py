from rest_framework import generics, response

from . import enums
from . import models
from . import serializers


class DonutNotFound(Exception):
    pass


class DonutList(generics.ListCreateAPIView):
    queryset = models.Donut.objects.all()
    serializer_class = serializers.DonutSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            qs = qs.filter(description__icontains=query)
        return qs


class DonutDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Donut.objects.all()
    serializer_class = serializers.DonutSerializer


class CreateOrder(generics.GenericAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.CreateOrderSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return response.Response(serializer.errors, status=400)
        try:
            create_order(serializer.validated_data)
        except DonutNotFound as e:
            return response.Response(data={"error": str(e)}, status=400)
        return response.Response(status=201)


class OrderList(generics.ListAPIView):
    queryset = models.Order.objects.all()
    serializer_class = serializers.ListOrderSerializer


def create_order(order_data):
    for order in order_data["donuts"]:
        try:
            donut = models.Donut.objects.get(code=order["donut_code"])
        except models.Donut.DoesNotExist:
            raise DonutNotFound(f"Donut code {order['donut_code']} not exist")
        models.Order.new(
            donut_code=donut,
            state=enums.OrderStatus.CREATED.value,
        )
