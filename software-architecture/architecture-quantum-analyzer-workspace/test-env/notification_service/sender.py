"""Notification sender — email and SMS dispatch.

Emphasizes AVAILABILITY: fire-and-forget with retry.
Failures are logged but never block the pipeline.
"""


def send_notification(event: dict) -> None:
    """Send notification for an auction event."""
    event_type = event.get("event", "unknown")

    if event_type == "auction_closed":
        _notify_winner(event)
    else:
        print(f"[Notification] Unknown event type: {event_type}")


def _notify_winner(event: dict) -> None:
    """Notify the auction winner via email and SMS."""
    winner = event.get("winner_id", "unknown")
    item = event.get("item_name", "unknown item")
    auction_id = event.get("auction_id", "???")

    # Simulate email
    print(f"[Email] To {winner}: You won '{item}' (auction {auction_id})!")
    # Simulate SMS
    print(f"[SMS] To {winner}: Congrats! You won auction {auction_id}.")
