# Structured Data Extractor

AI agent converting unstructured text/emails into validated JSON orders using Pydantic & Instructor.

## Setup & Installation

1. **Environment Variables**
   ```bash
   cp .env.example .env
   ```
   Fill in your `OPENAI_API_KEY` in the `.env` file.

2. **Install Dependencies**
   ```bash
   uv sync
   ```

## Running the App

Run the server on port 8001 (to avoid conflict with other services):

```bash
uv run uvicorn main:app --port 8001 --reload
```

## Testing the API

### Parse Order (AI Extraction)

Extracts structured JSON from unstructured text.

**Request:**
```bash
curl -X POST "http://localhost:8001/parse-order" \
     -H "Content-Type: application/json" \
     -d '{
       "text": "Dear Admin, please send me 3 units of MacBook Pro M3. I need it by tomorrow, so please use Overnight shipping. My name is Alex from TechCorp."
     }'
```

**Response:**
```json
{
  "customer_name": "Alex from TechCorp",
  "items": [
    {
      "product_name": "MacBook Pro M3",
      "quantity": 3
    }
  ],
  "shipping": "overnight",
  "notes": null
}
```