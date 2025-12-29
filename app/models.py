from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from enum import Enum


class ShippingMethod(str, Enum):
    REGULAR = "regular"
    EXPRESS = "express"
    OVERNIGHT = "overnight"


class OrderItem(BaseModel):
    product_name: str = Field(..., description="Name of the ordered product")
    quantity: int = Field(..., description="Quantity of items")

    @field_validator("quantity")
    def check_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be greater than 0")
        return v


class OrderExtraction(BaseModel):
    customer_name: str = Field(..., description="Full name of the customer")
    items: List[OrderItem] = Field(..., description="List of items in the order")
    shipping: ShippingMethod = Field(..., description="Selected shipping method")
    notes: Optional[str] = Field(
        None, description="Additional notes or Special requests"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "customer_name": "John Doe",
                    "items": [
                        {"product_name": "Premium Keyboard", "quantity": 1},
                        {"product_name": "USB-C Cable", "quantity": 2},
                    ],
                    "shipping": "express",
                    "notes": "Deliver before 5 PM",
                }
            ]
        }
    }


class ParseRequest(BaseModel):
    text: str = Field(..., description="Raw text from email or invoice to parse.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "text": "Order from Alice. She wants 2 laptops via overnight shipping."
                }
            ]
        }
    }
