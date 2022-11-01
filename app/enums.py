from choicesenum import ChoicesEnum


class OrderStatus(ChoicesEnum):
    CREATED = "Created"
    DISPATCHED = "Dispatched"


class Channel(ChoicesEnum):
    ORDER = "Order"
    DONUT = "Donut"


class Action(ChoicesEnum):
    DONUT_CREATED = "Created"
    UPDATED = "Updated"
