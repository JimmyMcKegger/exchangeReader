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
    created_at: str
    completed_at: str

    def __str__(self) -> str:
        return (
            f"\nOrder {self.order_id}:\n"
            f"Exchange Type: {self.exchange_type.value}\n"
            f"Original Amount: ${self.original_amount}\n"
            f"New Amount: ${self.new_amount}\n"
            f"Original SKU: {self.original_sku}\n"
            f"New SKU: {self.new_sku}\n"
            f"Created At: {self.created_at}\n"
            f"Completed At: {self.completed_at}"
        )
