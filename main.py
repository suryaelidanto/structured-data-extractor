import os
from enum import Enum
from typing import List
from pydantic import BaseModel, Field, field_validator
import instructor
from openai import OpenAI
import dotenv

dotenv.load_dotenv()

client = instructor.from_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))


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
    customer_name: str
    items: List[OrderItem]
    shipping: ShippingMethod
    notes: str = Field(..., description="Additional notes; if none, specify 'None'")


email_content = """
Hi Admin,
I'd like to order 5 units of ASUS ROG Gaming Laptops for my esports team.
Please also include 10 Logitech G Pro mice.
Since we have a tournament the day after tomorrow, could you please ship these as soon as possible?
Ideally, they should arrive tomorrow. No delays, please.

Best regards,
Budi Santoso (PT Maju Mundur)
"""

print("Processing customer order...")

order_data = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=OrderExtraction,
    messages=[
        {
            "role": "system",
            "content": "You are a perfect order parser. Extract data accurately.",
        },
        {"role": "user", "content": email_content},
    ],
)

print("\n=== EXTRACTION RESULTS ===")
print(f"Customer:  {order_data.customer_name}")
print(f"Shipping:  {order_data.shipping}")
print(f"Notes:     {order_data.notes}")
print("-" * 25)
print("Item List:")
for item in order_data.items:
    print(f"- {item.product_name} (Qty: {item.quantity})")

print("\n=== Raw JSON (Ready for Database) ===")
print(order_data.model_dump_json(indent=2))
