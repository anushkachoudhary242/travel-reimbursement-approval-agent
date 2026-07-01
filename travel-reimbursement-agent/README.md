# 🚀 AI Travel Reimbursement Approval Agent

An AI-powered Travel Reimbursement Approval System built using **FastAPI, LangGraph, Google Gemini, LangChain, and ChromaDB (RAG)**.

The system automates travel reimbursement claim processing by validating expenses against company policy, checking receipts, retrieving relevant policy sections using RAG, applying deterministic business rules, and generating AI-powered explanations.

---

# ✨ Features

- ✅ FastAPI REST API
- ✅ LangGraph Workflow
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ ChromaDB Vector Database
- ✅ Google Gemini Integration
- ✅ Deterministic Business Decision Engine
- ✅ Receipt Validation
- ✅ Duplicate Receipt Detection
- ✅ Expense Limit Validation
- ✅ Automatic Approver Selection
- ✅ AI Generated Explanation
- ✅ Modular Architecture
- ✅ Swagger Documentation

---

# 🏗 Project Architecture

```
                Claim Request
                      │
                      ▼
               FastAPI Endpoint
                      │
                      ▼
               LangGraph Workflow
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
 Policy Retrieval   Receipt Check   Limit Check
      │               │                │
      └───────────────┼────────────────┘
                      ▼
           Duplicate Receipt Check
                      │
                      ▼
          Required Approver Detection
                      │
                      ▼
       Business Decision Engine (Python)
                      │
                      ▼
             Google Gemini Explanation
                      │
                      ▼
               Final JSON Response
```

---

# 📁 Project Structure

```
travel-reimbursement-agent/

│
├── app/
│   ├── agent.py
│   ├── graph.py
│   ├── rag.py
│   ├── tools.py
│   ├── decision_engine.py
│   ├── prompts.py
│   ├── schemas.py
│   ├── state.py
│   ├── main.py
│   ├── config.py
│   ├── logger.py
│   ├── exceptions.py
│
├── data/
│   ├── policy.md
│   ├── limits.json
│   ├── approval_matrix.json
│   ├── receipts_db.json
│   ├── receipts_index.json
│   │
│   └── claims/
│       ├── approved.json
│       ├── partial.json
│       ├── rejected.json
│       └── manual_review.json
│
├── tests/
│
├── chroma_db/
│
├── streamlit_app.py
│
├── requirements.txt
│
└── README.md
```

---

# ⚙️ Technologies Used

- Python 3.12
- FastAPI
- LangGraph
- LangChain
- Google Gemini
- ChromaDB
- HuggingFace Embeddings
- Sentence Transformers
- Streamlit
- Pydantic

---

# 🧠 AI Workflow

## Step 1

Receive Travel Claim

Example

```json
{
  "employee_id":"EMP001",
  "employee_name":"Rahul Sharma",
  "trip_location":"Mumbai",
  "hotel":6000,
  "meal":900,
  "taxi":800,
  "flight":"Economy",
  "flight_amount":12000,
  "shopping":0,
  "receipts":[
      "receipt_001",
      "receipt_002",
      "receipt_003"
  ]
}
```

---

## Step 2

Retrieve Relevant Policy

The policy document is:

```
policy.md
```

The document is

- Loaded
- Chunked
- Embedded
- Stored in ChromaDB

The user's claim is converted into a semantic query.

Example:

```
Hotel:6000
Meal:900
Taxi:800
Flight:Economy
```

Top relevant chunks are retrieved using ChromaDB.

---

## Step 3

Expense Validation

The following company limits are loaded

```
limits.json
```

Example

Hotel

₹7000/night

Meal

₹1000/day

Taxi

₹5000

Flight

Economy Only

---

## Step 4

Receipt Validation

The system validates

- Receipt exists
- Attachment exists

If attachment is missing

↓

Manual Review

---

## Step 5

Duplicate Receipt Detection

Duplicate receipt IDs are rejected immediately.

---

## Step 6

Required Approver

Approval Matrix

```
≤ ₹10,000
Manager

₹10,001–₹50,000
Senior Manager

> ₹50,000
Director
```

---

## Step 7

Business Decision Engine

This project **does NOT allow the LLM to calculate reimbursement amounts**.

All reimbursement calculations are deterministic and implemented in Python.

### Rules

### Hotel

If claimed amount exceeds policy

Approve up to policy limit

Reject excess amount

---

### Meal

Approve up to ₹1000/day

Reject remaining amount

---

### Taxi

Approve up to ₹5000

Reject remaining amount

---

### Flight

Economy

✅ Reimbursable

Business

❌ Not Reimbursable

---

### Shopping

Shopping is a personal expense.

Always rejected.

---

### Missing Receipt

↓

Manual Review

---

### Duplicate Receipt

↓

Reject Entire Claim

---

## Step 8

Google Gemini

Gemini DOES NOT make financial decisions.

Gemini only generates

- Explanation
- Confidence
- Policy References

---

# 🤖 Why a Business Decision Engine?

Financial calculations should always be deterministic.

Large Language Models are probabilistic and may produce inconsistent reimbursement calculations.

Therefore,

Python performs

- Expense validation
- Financial calculations
- Business rules

Gemini only explains the decision.

This architecture improves

- Consistency
- Auditability
- Reliability
- Explainability

---

# 📦 API

## Health

GET

```
/health
```

---

## Evaluate Claim

POST

```
/evaluate
```

---

# Example Response

```json
{
    "decision":"Partially Approved",

    "approved_amount":20900,

    "rejected_amount":4600,

    "approver":"Senior Manager",

    "confidence":0.98,

    "expenses":[
        {
            "category":"Hotel",
            "claimed":10000,
            "approved":7000,
            "rejected":3000,
            "status":"Partially Approved",
            "remarks":"Exceeded hotel reimbursement limit"
        },
        {
            "category":"Meal",
            "claimed":2000,
            "approved":1000,
            "rejected":1000,
            "status":"Partially Approved",
            "remarks":"Exceeded meal reimbursement limit"
        },
        {
            "category":"Taxi",
            "claimed":900,
            "approved":900,
            "rejected":0,
            "status":"Approved",
            "remarks":"Within limit"
        },
        {
            "category":"Flight",
            "claimed":12000,
            "approved":12000,
            "rejected":0,
            "status":"Approved",
            "remarks":"Economy class"
        },
        {
            "category":"Shopping",
            "claimed":600,
            "approved":0,
            "rejected":600,
            "status":"Rejected",
            "remarks":"Personal expenses are not reimbursable"
        }
    ],

    "explanation":"The hotel and meal expenses exceeded policy limits and were partially reimbursed. Taxi and economy flight expenses complied with company policy. Shopping expenses are personal in nature and therefore rejected."
}
```

---

# ▶️ Running the Project

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Start FastAPI

```bash
uvicorn app.main:app --reload
```

Swagger

```
http://127.0.0.1:8000/docs
```

---

## (Optional) Run Streamlit

```bash
streamlit run streamlit_app.py
```


# 📌 Future Improvements

- OCR-based receipt extraction
- Invoice fraud detection
- Multi-policy support
- PostgreSQL integration
- Authentication & Authorization
- Cloud deployment
- LangSmith tracing
- Docker support

---

# 👨‍💻 Author

Developed as an AI Engineering assignment demonstrating:

- FastAPI
- LangGraph
- RAG
- ChromaDB
- Google Gemini
- Deterministic Decision Engine
- Modular AI Workflow