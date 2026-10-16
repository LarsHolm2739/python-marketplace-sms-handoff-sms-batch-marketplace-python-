import json

from .infrai_client import InfraiClient
from .marketplace_campaign import BuyerUpdate, SellerAsset, send_campaign


def main() -> None:
    asset = SellerAsset(sku="KIT-42", title="Home test kit")
    updates = [BuyerUpdate(phone="+15550101", order_id="ORD-1001", asset=asset)]
    print(json.dumps(send_campaign(updates, InfraiClient()), indent=2))


if __name__ == "__main__":
    main()
