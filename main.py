from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from enum import Enum
import instructor
from openai import OpenAI
import os
import dotenv
import uvicorn

dotenv.load_dotenv()

client = instructor.from_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))

app = FastAPI(
    title="Invoice Parser Agent API",
    description="AI-powered engine to extract structured order data from emails or invoices.",
)


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
    notes: Optional[str] = Field(
        ..., description="Additional notes; if none, specify 'None'"
    )


class ParseRequest(BaseModel):
    text: str = Field(..., description="The raw text of the email or invoice to parse.")


@app.get("/")
def health_check():
    return {"status": "ok", "service": "Invoice Parser Agent"}


@app.post("/parse-order", response_model=OrderExtraction)
def parse_order_endpoint(data: ParseRequest):
    """
    Extracts structured order information from raw text using AI.
    """
    order_data = client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=OrderExtraction,
        messages=[
            {
                "role": "system",
                "content": "You are a perfect order parser. Extract data accurately from the provided text into the specified JSON format.",
            },
            {"role": "user", "content": data.text},
        ],
    )
    return order_data


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
