from dataclasses import dataclass
from models.exchangeType import ExchangeType


@dataclass
class Exchange:
    order_id: str
    exchange_id: str
    original_amount: float
    new_amount: float
    original_sku: str
    new_sku: str
    exchange_type: ExchangeType

    def __str__(self):
        return f"""
            Order ID: {self.order_id}
            Exchange ID: {self.exchange_id}
            Original Amount: {self.original_amount}
            New Amount: {self.new_amount}
            Original SKU: {self.original_sku}
            New SKU: {self.new_sku}
            Exchange Type: {self.exchange_type}
        """
