import stripe
import os

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

PRICES = {
    "baron":      {"amount": 900,  "label": "Baron Profile — Sterling Sovereign"},
    "duke":       {"amount": 2900, "label": "Duke Profile — Sterling Sovereign"},
    "chancellor": {"amount": 9900, "label": "Chancellor Profile — Sterling Sovereign"},
}


def create_checkout_session(tier: str, metadata: dict, success_url: str, cancel_url: str) -> str:
    price = PRICES.get(tier, PRICES["duke"])
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "gbp",
                "unit_amount": price["amount"],
                "product_data": {
                    "name": price["label"],
                    "description": f"AI-generated Sovereign wealth identity ({tier.capitalize()} tier).",
                },
            },
            "quantity": 1,
        }],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
        metadata=metadata,
        customer_email=metadata.get("email"),
    )
    return session.url


def verify_session(session_id: str) -> dict:
    session = stripe.checkout.Session.retrieve(session_id)
    if session.payment_status != "paid":
        raise ValueError(f"Payment not completed: {session.payment_status}")
    return dict(session.metadata)


def construct_webhook_event(payload: bytes, sig_header: str) -> stripe.Event:
    secret = os.environ.get("STRIPE_WEBHOOK_SECRET")
    return stripe.Webhook.construct_event(payload, sig_header, secret)
