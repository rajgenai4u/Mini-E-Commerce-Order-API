from typing import List
from uuid import uuid4
from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas

app = FastAPI(
    title="Mini E-Commerce Order API (Neon DB)",
    description="FastAPI application connected to Neon PostgreSQL database.",
    version="1.0.0"
)

# Allowed status state transitions
ALLOWED_TRANSITIONS = {
    models.OrderStatus.PLACED: [models.OrderStatus.PROCESSING],
    models.OrderStatus.PROCESSING: [models.OrderStatus.SHIPPED],
    models.OrderStatus.SHIPPED: [models.OrderStatus.DELIVERED],
    models.OrderStatus.DELIVERED: []
}

# ------------------------------------------------------------------------------
# Product Endpoints
# ------------------------------------------------------------------------------

@app.post("/products", response_model=schemas.ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(product_in: schemas.ProductCreate, db: Session = Depends(get_db)):
    product_id = str(uuid4())
    db_product = models.Product(
        id=product_id,
        name=product_in.name,
        price=product_in.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products", response_model=List[schemas.ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

# ------------------------------------------------------------------------------
# Order Endpoints
# ------------------------------------------------------------------------------

@app.post("/orders", response_model=schemas.OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order_in: schemas.OrderCreate, db: Session = Depends(get_db)):
    if not order_in.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must contain at least one item."
        )

    order_id = str(uuid4())
    total_amount = 0.0
    db_order_items = []

    # Validate each item and calculate server-side subtotal
    for item in order_in.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with ID '{item.product_id}' not found."
            )

        if item.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid quantity {item.quantity} for product '{product.name}'."
            )

        subtotal = round(float(product.price) * item.quantity, 2)
        total_amount += subtotal

        db_order_items.append(
            models.OrderItem(
                id=str(uuid4()),
                order_id=order_id,
                product_id=product.id,
                product_name=product.name,
                unit_price=product.price,
                quantity=item.quantity,
                subtotal=subtotal
            )
        )

    db_order = models.Order(
        id=order_id,
        customer_name=order_in.customer_name,
        total_amount=round(total_amount, 2),
        status=models.OrderStatus.PLACED
    )

    db.add(db_order)
    db.add_all(db_order_items)
    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/orders", response_model=List[schemas.OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return db.query(models.Order).all()


@app.get("/orders/{order_id}", response_model=schemas.OrderResponse)
def get_order(order_id: str, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID '{order_id}' not found."
        )
    return order


@app.put("/orders/{order_id}/status", response_model=schemas.OrderResponse)
def update_order_status(order_id: str, status_update: schemas.OrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID '{order_id}' not found."
        )

    current_status = order.status
    new_status = status_update.status

    if new_status not in ALLOWED_TRANSITIONS[current_status]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid transition from {current_status.value} to {new_status.value}. "
                   f"Allowed: {[s.value for s in ALLOWED_TRANSITIONS[current_status]]}"
        )

    order.status = new_status
    db.commit()
    db.refresh(order)
    return order