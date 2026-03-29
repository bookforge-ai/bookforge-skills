"""Payment processing logic.

Emphasizes RELIABILITY (idempotent processing, audit trail)
and SECURITY (input validation, amount verification).
"""

from pydantic import BaseModel, field_validator

# Audit log (in production: durable database)
processed_auctions: set = set()


class PaymentEvent(BaseModel):
    event: str
    auction_id: str
    winner_id: str
    amount: float

    @field_validator("amount")
    @classmethod
    def amount_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Payment amount must be positive")
        return v


def process_payment(raw: dict) -> None:
    """Process a payment — idempotent to ensure reliability."""
    event = PaymentEvent(**raw)

    # Idempotency check
    if event.auction_id in processed_auctions:
        print(f"[Payment] Already processed {event.auction_id}, skipping")
        return

    # Simulate payment gateway call
    print(f"[Payment] Charging {event.winner_id} ${event.amount:.2f} "
          f"for auction {event.auction_id}")

    processed_auctions.add(event.auction_id)
    print(f"[Payment] Completed for auction {event.auction_id}")
