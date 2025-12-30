import os
import instructor
from openai import OpenAI
from app.models import OrderExtraction

from dotenv import load_dotenv

load_dotenv()

client = instructor.from_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))


def parse_order_from_text(text: str) -> OrderExtraction:
    """Extract structured order data from raw text using LLM."""
    return client.chat.completions.create(
        model="gpt-4o-mini",
        response_model=OrderExtraction,
        messages=[
            {
                "role": "system",
                "content": "You are a specialized order parser. Extract data accurately into the specified JSON format. If customer name is missing, use 'Unknown'.",
            },
            {"role": "user", "content": text},
        ],
    )
