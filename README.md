# Shopify Exchange Analyzer

A Python tool to analyze exchanges on Shopify orders and categorize them based on price differences and SKU changes.

## Prerequisites

- Python 3.10 or higher
- Poetry (Python package manager)
- [Custom Shopify app with Admin API access](https://shopify.dev/docs/apps/build/authentication-authorization/access-tokens/generate-app-access-tokens-admin)
- [ExchangeV2 API access](https://shopify.dev/docs/apps/build/pos/exchangesv2)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/JimmyMcKegger/exchangeReader.git
```

2. Install dependencies:
```bash
poetry install
```

## Configuration

1. Copy the example environment file:

```bash
cp .env.example .env
```

2. Set the Shopify shop URL and access token in the `.env` file.

3. Request ExchangeV2 API access if necessary.

## Usage

1. Edit src/main.py to include the order IDs you want to analyze:

```python
ORDERS = ["6433022181710", "6412659065166", "6433024803150"]
```

2. Run the script:

```bash
poetry run python src/main.py
```

### Exchange Categories

The tool categorizes exchanges into three types:

- Customer Paid Difference: When the new item costs more than the original
- Customer Was Refunded Difference: When the new item costs less than the original
- Exchanged for Same SKU: When the same product was exchanged (e.g., different size)
