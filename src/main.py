from dotenv import load_dotenv
from models import ShopifyExchangeReader

load_dotenv()

ORDERS = ["6433022181710", "6412659065166", "6433024803150", "6401803682126"]


def main():
    reader = ShopifyExchangeReader()

    for order_id in ORDERS:
        try:
            exchanges = reader.handle_exchanges(order_id)
            for exchange in exchanges:
                print(exchange)
        except Exception as e:
            print(f"Error processing order {order_id}: {str(e)}")


if __name__ == "__main__":
    main()
