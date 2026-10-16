from dataclasses import dataclass
from typing import Dict, List

from .infrai_client import InfraiClient


@dataclass(frozen=True)
class SellerAsset:
    sku: str
    title: str


@dataclass(frozen=True)
class BuyerUpdate:
    phone: str
    order_id: str
    asset: SellerAsset


def send_campaign(updates: List[BuyerUpdate], client: InfraiClient) -> List[Dict[str, str]]:
    """Send one concise order handoff per buyer and return delivery states."""
    results: List[Dict[str, str]] = []
    for update in updates:
        text = f"Order {update.order_id}: {update.asset.title} is ready for handoff."
        sent = client.send_sms(update.phone, text)
        message_id = str(sent["message_id"])
        status = client.sms_status(message_id)
        results.append({"order_id": update.order_id, "message_id": message_id, "status": str(status.get("status", "queued"))})
    return results
