import os
from typing import Dict, List
from models.exchange import Exchange
from models.exchangeType import ExchangeType
from pathlib import Path
import requests


class ShopifyExchangeReader:
    def __init__(self):
        self.shop_url = os.getenv("SHOPIFY_SHOP_URL")
        self.access_token = os.getenv("SHOPIFY_ACCESS_TOKEN")

    def _load_query(self) -> str:
        query_path = Path(__file__).parent.parent / "queries" / "orderQuery.graphql"
        with open(query_path, "r") as f:
            return f.read()

    def get_headers(self) -> Dict:
        return {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": self.access_token,
        }

    def analyze_exchange(self, order_data: Dict) -> List[Exchange]:
        """
        Analyzes completed exchanges from a Shopify order and categorizes each exchange.

        This method processes exchange data to determine:
        - If a customer paid more for a new item
        - If a customer was refunded for choosing a cheaper item
        - If the exchange was for the same SKU (e.g., different size)

        Only processes exchanges that are marked as completed (completed_at is not empty)
        as incomplete exchanges may have incomplete data.

        Args:
            order_data (Dict): Raw order data from Shopify containing exchange information

        Returns:
            List[Exchange]: A list of Exchange objects containing categorized exchange data
        """
        exchanges = []

        if not order_data or "exchangeV2s" not in order_data:
            return exchanges

        for exchange in order_data["exchangeV2s"]["nodes"]:
            # Skip exchanges that aren't completed
            if not exchange.get("completedAt"):
                continue

            # Skip exchanges without complete line item information
            if (
                not exchange["additions"]["lineItems"]
                or not exchange["returns"]["lineItems"]
            ):
                continue

            new_item = exchange["additions"]["lineItems"][0]
            returned_item = exchange["returns"]["lineItems"][0]

            new_amount = float(new_item["originalTotalSet"]["shopMoney"]["amount"])
            original_amount = abs(
                float(exchange["returns"]["totalPriceSet"]["shopMoney"]["amount"])
            )
            new_sku = new_item["sku"]
            original_sku = returned_item["lineItem"]["sku"]

            exchange_type = self._determine_exchange_type(
                original_amount, new_amount, original_sku, new_sku
            )

            exchanges.append(
                Exchange(
                    order_id=order_data["id"],
                    exchange_id=exchange["id"],
                    original_amount=original_amount,
                    new_amount=new_amount,
                    original_sku=original_sku,
                    new_sku=new_sku,
                    exchange_type=exchange_type,
                    created_at=exchange["createdAt"],
                    completed_at=exchange["completedAt"],
                )
            )

        return exchanges

    def _determine_exchange_type(
        self, original_amount: float, new_amount: float, original_sku: str, new_sku: str
    ) -> ExchangeType:
        if original_sku == new_sku:
            return ExchangeType.SAME_SKU
        elif new_amount > original_amount:
            return ExchangeType.PAID_DIFFERENCE
        elif new_amount < original_amount:
            return ExchangeType.REFUNDED_DIFFERENCE
        return ExchangeType.UNKNOWN

    def handle_exchanges(self, order_id: str) -> List[Exchange]:
        variables = {"orderId": f"gid://shopify/Order/{order_id}"}

        response = requests.post(
            f"{self.shop_url}/admin/api/2025-01/graphql.json",
            headers=self.get_headers(),
            json={"query": self._load_query(), "variables": variables},
        )

        if response.status_code == 200:
            data = response.json()
            return self.analyze_exchange(data["data"]["order"])
        else:
            raise Exception(f"Failed to fetch order: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            return self.analyze_exchange(data["data"]["order"])
        else:
            raise Exception(f"Failed to fetch order: {response.status_code}")
