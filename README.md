# Structured Data Extractor

![CI Status](https://github.com/suryaelidanto/structured-data-extractor/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

An AI-powered microservice designed to transform unstructured text (emails, invoices, chat logs) into strictly validated, structured data schemas.

## Features
- **Schema Enforcement**: Uses Pydantic V2 to ensure parsed data matches your business rules.
- **Smart Parsing**: Powered by GPT-4o-mini and `instructor` for high-accuracy extraction.
- **Input Validation**: Custom Pydantic validators to catch logical errors (e.g., negative quantities).
- **Production Infrastructure**: Built-in Docker, Makefile, and CI/CD support.

---

## Prerequisites
- **Python**: 3.10+
- **UV**: Fast Python package manager
- **OpenAI API Key**: Required for the parsing engine

---

## Usage

### 1. Configuration
Create a `.env` file:
```text
OPENAI_API_KEY=sk-...
```

### 2. Run API
```bash
make dev
```
Access the interactive documentation at `http://localhost:8000/docs`.

### 3. API Scenarios

#### Scenario: Extracting Order from Email
**Request:** `POST /parse-order`
```json
{
  "text": "Hi, I'm John. I want to buy 3 mechanical keyboards and I need express shipping. Please leave it at the front door."
}
```
**Output:**
```json
{
  "customer_name": "John",
  "items": [
    {
      "product_name": "mechanical keyboards",
      "quantity": 3
    }
  ],
  "shipping": "express",
  "notes": "Please leave it at the front door."
}
```

---

## Roadmap
- [x] Order extraction logic with Pydantic validation.
- [x] FastAPI modularization.
- [ ] Multi-document support (Batch parsing).
- [ ] Table extraction from raw text/markdown.

---

## Development
- **Linting**: `make lint`
- **Testing**: `make test`
- **Docker**: `make up`