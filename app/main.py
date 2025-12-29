from fastapi import FastAPI, HTTPException
from app.models import ParseRequest, OrderExtraction
from app.services import parse_order_from_text

app = FastAPI(
    title="Structured Data Extractor API",
    description="AI-powered engine to transform unstructured text into validated order schemas.",
    version="1.0.0",
)


@app.get("/")
async def health_check():
    return {"status": "ok", "service": "Structured Data Extractor"}


@app.post("/parse-order", response_model=OrderExtraction)
async def parse_order(data: ParseRequest):
    """Transform raw email/invoice text into structured order data."""
    try:
        result = parse_order_from_text(data.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing Error: {str(e)}")
