"""Bidder Service — handles bid placement.

Architecture characteristics: ELASTICITY (burst traffic), PERFORMANCE (low latency).
Communication: synchronous REST calls to Auction Service (same quantum).
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import httpx

app = FastAPI(title="Bidder Service")

AUCTION_SERVICE_URL = "http://auction:8002"  # synchronous coupling


class BidRequest(BaseModel):
    auction_id: str
    bidder_id: str
    amount: float


class BidResponse(BaseModel):
    bid_id: str
    status: str
    current_price: float


@app.post("/bids", response_model=BidResponse)
async def place_bid(bid: BidRequest):
    """Place a bid — calls Auction Service synchronously to validate and record."""
    # SYNC call: tight coupling with Auction Service (same quantum)
    async with httpx.AsyncClient(timeout=2.0) as client:
        resp = await client.post(
            f"{AUCTION_SERVICE_URL}/auctions/{bid.auction_id}/bids",
            json={"bidder_id": bid.bidder_id, "amount": bid.amount},
        )
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.json())
    data = resp.json()
    return BidResponse(
        bid_id=data["bid_id"],
        status=data["status"],
        current_price=data["current_price"],
    )


@app.get("/bids/{auction_id}")
async def get_bids(auction_id: str):
    """Fetch current bids — proxied from Auction Service synchronously."""
    async with httpx.AsyncClient(timeout=2.0) as client:
        resp = await client.get(
            f"{AUCTION_SERVICE_URL}/auctions/{auction_id}/bids"
        )
    return resp.json()


@app.get("/health")
async def health():
    return {"status": "ok", "service": "bidder"}
