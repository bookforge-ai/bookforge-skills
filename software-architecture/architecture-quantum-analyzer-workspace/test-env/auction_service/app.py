"""Auction Service — manages auction lifecycle.

Architecture characteristics: moderate (inherits elasticity needs from Bidder coupling).
Communication:
  - Receives synchronous REST from Bidder Service (same quantum).
  - Publishes asynchronous events to Payment and Notification via RabbitMQ (different quanta).
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from events import publish_event

app = FastAPI(title="Auction Service")

# In-memory store (mock)
auctions: dict = {}
bid_counter = 0


class Auction(BaseModel):
    auction_id: str
    item_name: str
    starting_price: float
    status: str = "active"
    current_price: float = 0.0


class IncomingBid(BaseModel):
    bidder_id: str
    amount: float


@app.post("/auctions")
async def create_auction(auction: Auction):
    auctions[auction.auction_id] = {
        "item_name": auction.item_name,
        "starting_price": auction.starting_price,
        "current_price": auction.starting_price,
        "status": "active",
        "bids": [],
    }
    return {"auction_id": auction.auction_id, "status": "created"}


@app.post("/auctions/{auction_id}/bids")
async def accept_bid(auction_id: str, bid: IncomingBid):
    """Accept bid from Bidder Service (synchronous — same quantum)."""
    global bid_counter
    if auction_id not in auctions:
        raise HTTPException(404, "Auction not found")
    auction = auctions[auction_id]
    if auction["status"] != "active":
        raise HTTPException(400, "Auction is not active")
    if bid.amount <= auction["current_price"]:
        raise HTTPException(400, "Bid must exceed current price")

    bid_counter += 1
    bid_id = f"BID-{bid_counter:04d}"
    auction["current_price"] = bid.amount
    auction["bids"].append(
        {"bid_id": bid_id, "bidder_id": bid.bidder_id, "amount": bid.amount}
    )
    return {"bid_id": bid_id, "status": "accepted", "current_price": bid.amount}


@app.get("/auctions/{auction_id}/bids")
async def list_bids(auction_id: str):
    if auction_id not in auctions:
        raise HTTPException(404, "Auction not found")
    return auctions[auction_id]["bids"]


@app.post("/auctions/{auction_id}/close")
async def close_auction(auction_id: str):
    """Close auction and emit async events to Payment and Notification quanta."""
    if auction_id not in auctions:
        raise HTTPException(404, "Auction not found")
    auction = auctions[auction_id]
    auction["status"] = "closed"
    winner = auction["bids"][-1] if auction["bids"] else None

    # ASYNC events — crosses quantum boundaries via message queue
    if winner:
        publish_event("payment_queue", {
            "event": "auction_closed",
            "auction_id": auction_id,
            "winner_id": winner["bidder_id"],
            "amount": winner["amount"],
        })
        publish_event("notification_queue", {
            "event": "auction_closed",
            "auction_id": auction_id,
            "winner_id": winner["bidder_id"],
            "item_name": auction["item_name"],
        })

    return {"auction_id": auction_id, "status": "closed", "winner": winner}


@app.get("/health")
async def health():
    return {"status": "ok", "service": "auction"}
