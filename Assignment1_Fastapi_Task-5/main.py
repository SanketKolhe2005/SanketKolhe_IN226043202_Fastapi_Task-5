from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Working"}

# ---------------- SAMPLE DATA ----------------
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 499, "category": "Electronics"},
    {"id": 2, "name": "Notebook", "price": 99, "category": "Stationery"},
    {"id": 3, "name": "USB Hub", "price": 799, "category": "Electronics"},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery"},
]

orders = []

# ---------------- EXISTING APIs ----------------

@app.get("/products/search")
def search_products(keyword: str):
    result = [p for p in products if keyword.lower() in p["name"].lower()]
    if not result:
        return {"message": f"No products found for: {keyword}"}
    return {"total_found": len(result), "products": result}


@app.get("/products/sort")
def sort_products(sort_by: str = "price", order: str = "asc"):
    if sort_by not in ["price", "name"]:
        return {"error": "sort_by must be 'price' or 'name'"}

    result = sorted(products, key=lambda p: p[sort_by], reverse=(order == "desc"))
    return {"sort_by": sort_by, "order": order, "products": result}


@app.get("/products/page")
def paginate_products(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    return {
        "page": page,
        "limit": limit,
        "total_pages": -(-len(products) // limit),
        "products": products[start:start + limit]
    }


@app.post("/orders")
def create_order(customer_name: str):
    order = {
        "order_id": len(orders) + 1,
        "customer_name": customer_name
    }
    orders.append(order)
    return order


# ---------------- Q4 ----------------
@app.get("/orders/search")
def search_orders(customer_name: str):
    result = [
        o for o in orders
        if customer_name.lower() in o["customer_name"].lower()
    ]

    if not result:
        return {"message": f"No orders found for: {customer_name}"}

    return {
        "customer_name": customer_name,
        "total_found": len(result),
        "orders": result
    }


# ---------------- Q5 ----------------
@app.get("/products/sort-by-category")
def sort_by_category():
    result = sorted(products, key=lambda p: (p["category"], p["price"]))
    return {"products": result, "total": len(result)}


# ---------------- Q6 ----------------
@app.get("/products/browse")
def browse_products(
    keyword: str = Query(None),
    sort_by: str = "price",
    order: str = "asc",
    page: int = 1,
    limit: int = 4
):
    result = products

    # SEARCH
    if keyword:
        result = [p for p in result if keyword.lower() in p["name"].lower()]

    # SORT
    if sort_by in ["price", "name"]:
        result = sorted(result, key=lambda p: p[sort_by], reverse=(order == "desc"))

    # PAGINATION
    total = len(result)
    start = (page - 1) * limit
    paged = result[start:start + limit]

    return {
        "keyword": keyword,
        "sort_by": sort_by,
        "order": order,
        "page": page,
        "limit": limit,
        "total_found": total,
        "total_pages": -(-total // limit),
        "products": paged
    }
