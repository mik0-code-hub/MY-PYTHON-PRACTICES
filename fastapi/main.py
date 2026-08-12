from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def read_root():
    return {'Hello': 'World'}
@app.get("/products/{prod_id}")
async def read_product(prod_id: int, discount: float= 0.0):
    if discount < 10:
        msg = f"Product '{prod_id}' is on Discount of ({discount}%)"
    else:
        msg = f"The product {prod_id} is not on Discount."
    return {
        "product_id":  prod_id,
        "discount":  discount,
        "message":  msg
    }