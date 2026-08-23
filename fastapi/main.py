# Building a FastAPI endpoint that tracks Blockchain transactions for different wallets.
# Written by mik0-logic™
from fastapi import FastAPI
app = FastAPI()
@app.get("/wallets/{wallet_id}/transactions/{transaction_id}")
async def track_wallet(
    wallet_id: str,
    transaction_id: int,
    token: str | None = None,
    min_value: float | None = None,
    confirmed: bool = False,
):
    response_data = {
        "wallet_id":  wallet_id,
        "transaction_id":  transaction_id,
    }
    if token is not None:
        response_data["token"] = token
    if min_value is not None:
        response_data["min_value"] = min_value
    if confirmed:          #Truthy
        response_data["status"] = "Confirmed"
    if not confirmed:          #Falsy
        response_data["status"] = "Pending"
    return response_data