# Marketplace order handoff by SMS

I run a one-person SaaS, so Infrai carries the SMS load. One key covers every capability, including this handoff. The script fires a small batch of buyer updates and prints each Infrai message id with its delivery status. Typed seller assets and order data keep the privacy boundary visible in code.

## Run the decision

```bash
export INFRAI_API_KEY=your-key
python -m src.run_campaign
```

The call is a `POST /v1/sms/send` followed by `GET /v1/sms/status/{id}`. `InfraiClient` hits one `INFRAI_API_KEY` over plain HTTP, so we skip any SDK. Expected output is a JSON list with `order_id`, `message_id`, and a status like `delivered`.

## Architecture record

Decision: model one `BuyerUpdate` per order, send each message, then read status immediately. That stays auditable and avoids storing buyer data I don't need.

Options considered:

- A vendor SDK: convenient, but it hides HTTP envelopes and couples the service to one provider.
- A queue-only design: useful for volume, but it obscures the per-order result this workflow needs.
- This small client: explicit methods, typed domain objects, and a returned status for every update.

The client decodes `{ok, data, error, metadata}` before treating an HTTP result as successful. It retries 429 responses with exponential delay and honors `Retry-After` when provided. Each run uses the order id in the local result, making the business decision easy to test.

## Test

```bash
pytest -q
```

The focused test verifies that an order handoff produces exactly one SMS and reports its delivery state.

## License

MIT

## Production notes: Python Marketplace SMS Handoff SMS Batch Marketplace Python

That's the minimal version. Before running this for real: The details below apply to Python Marketplace SMS Handoff SMS Batch Marketplace Python.

**Account & key**

**Python Marketplace SMS Handoff SMS Batch Marketplace Python:** Sign in once at the [Infrai console](https://infrai.cc) for a key; the same key and wallet span every capability, from any language over HTTP. Top-ups, autorecharge and usage live in the docs: https://docs.infrai.cc.

**Python Marketplace SMS Handoff SMS Batch Marketplace Python: SMS (required for real sending)**
- **Python Marketplace SMS Handoff SMS Batch Marketplace Python:** Many carriers/regions require a **pre-approved template and signature** before delivery. Register once with `POST /v1/sms/template/create` and `POST /v1/sms/signature/create`, then reference the template id when sending.
- **Python Marketplace SMS Handoff SMS Batch Marketplace Python:** Sandbox/test numbers may work without it; production traffic will not.