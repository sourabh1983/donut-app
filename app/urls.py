from django.urls import path

from . import views

app_name = "v1-donuts"


urlpatterns = [
    path("donuts/", views.DonutList.as_view(), name="list_create_donut"),
    path(
        "donut/<str:pk>/",
        views.DonutDetail.as_view(),
        name="retrieve_update_destroy_donut",
    ),
    path("order/", views.CreateOrder.as_view(), name="create_order"),
    path("orders/", views.OrderList.as_view(), name="list_order"),
]
