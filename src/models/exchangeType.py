from enum import Enum


class ExchangeType(Enum):
    PAID_DIFFERENCE = "Customer paid difference"
    REFUNDED_DIFFERENCE = "Customer was refunded difference"
    SAME_SKU = "Exchanged for same SKU"
    UNKNOWN = "Unknown exchange type"

    def __str__(self):
        return self.value
