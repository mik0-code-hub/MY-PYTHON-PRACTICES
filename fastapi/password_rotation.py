from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date

app = FastAPI()
class Account(BaseModel):
    account_name:  str
    last_updated:  date
    critical:  bool=False
    rotation_interval:  int=90
accounts = {}
@app.post("/accounts")
async def add_account(account: Account):
    accounts[account.account_name] = account
    return account
@app.get("/accounts")
async def list_accounts():
    return accounts
def calc_days_since_update(account: Account):
    days_since_update = (date.today() - account.last_updated).days
    return days_since_update
    # Written by mik0-logic™
@app.get("/accounts/rotation-status")
async def get_rotation_status():
    results = []
    for account in accounts.values():
        days = calc_days_since_update(account)
        if days >= account.rotation_interval:
            status = 'Overdue'
        else:
            status = 'Active'
        results.append({
            'account_name':  account.account_name,
            'days_since_update':  days,
            'rotation_interval':  account.rotation_interval,
            'status':  status
        })
    return results
@app.get("/accounts/{account_name}")
async def get_account_status(account_name: str):
    acct = accounts.get(account_name)
    if acct is None:
        return {"error": f"The account {account_name} not found!"}
    days = calc_days_since_update(acct)
    if days >= acct.rotation_interval:
        status = 'Overdue'
    else:
        status = 'Active'
    return {
        "account_name":  acct.account_name,
        "days_since_update":  days,
        "rotation_interval":  acct.rotation_interval,
        "status":  status
        # Written by mik0-logic™
    }
@app.put("/accounts/{account_name}")
async def update_account(account_name: str, account: Account):
    acct = accounts.get(account_name)
    if acct is None:
        return {"error": f"Account {account_name} not Found!"}
    accounts[account_name] = account
    return account
@app.delete("/accounts/{account_name}")
async def delete_account(account_name: str):
    if account_name not in accounts:
        return {"error": f"{account_name} not found."}
    del accounts[account_name]
    return {"message":  f"Account '{account_name}' deleted Successfully!"}