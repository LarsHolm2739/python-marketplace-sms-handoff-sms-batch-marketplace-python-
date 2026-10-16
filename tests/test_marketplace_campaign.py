from src.marketplace_campaign import BuyerUpdate, SellerAsset, send_campaign


class FakeClient:
    def __init__(self):
        self.sent = []

    def send_sms(self, to, message):
        self.sent.append((to, message))
        return {"message_id": "m-1"}

    def sms_status(self, message_id):
        return {"status": "delivered"}


def test_campaign_hands_off_each_order_and_reports_status():
    client = FakeClient()
    update = BuyerUpdate("+15550001", "ORD-9", SellerAsset("SKU-9", "Vitals monitor"))
    assert send_campaign([update], client) == [{"order_id": "ORD-9", "message_id": "m-1", "status": "delivered"}]
    assert client.sent == [("+15550001", "Order ORD-9: Vitals monitor is ready for handoff.")]
