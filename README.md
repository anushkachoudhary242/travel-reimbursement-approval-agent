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
  "employee_id": "EMP006",
  "employee_name": "Rohit",
  "trip_location": "Chennai",
  "hotel": 1500,
  "meal": 1000,
  "taxi": 800,
  "flight_type": "Economy",
  "flight_fare": 25000,
  "shopping": 0,
  "receipts": [
    "receipt_008"
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
Hotel Expense: ₹1500
Meal Expense: ₹1000
Taxi Expense: ₹800
Flight Type: Economy
Flight Fare: ₹25000
Shopping Expense: ₹0
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

- Receipt exists in the receipt database
- Receipt attachment is available
- Receipt IDs are valid

Business Rules

- If no receipts are uploaded for a claim containing reimbursable expenses, the claim is sent for Manual Review.
- If a referenced receipt does not exist, the claim is sent for Manual Review.
- If a receipt attachment is missing, the claim is sent for Manual Review.
- Valid receipts allow the reimbursement process to continue.

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

## Step 7: Business Decision Engine

The Travel Reimbursement Approval Agent uses a **deterministic Business Decision Engine** implemented entirely in Python.

Unlike Large Language Models, the Business Decision Engine performs all reimbursement calculations using predefined business rules, ensuring that financial decisions are consistent, auditable, and reliable.

Google Gemini is **not responsible for making reimbursement decisions**. It only generates a human-readable explanation based on the final decision produced by the Business Decision Engine.

---

## Business Rules

### 🏨 Hotel Reimbursement

**Policy Limit:** ₹7,000 per night

**Rules**

- Hotel expense less than or equal to ₹7,000 → Fully Approved
- Hotel expense greater than ₹7,000 → Approve up to ₹7,000 and reject the remaining amount

**Example**

| Claimed | Approved | Rejected |
|---------:|---------:|---------:|
| ₹6,000 | ₹6,000 | ₹0 |
| ₹8,500 | ₹7,000 | ₹1,500 |

---

### 🍽 Meal Reimbursement

**Policy Limit:** ₹1,000 per day

**Rules**

- Meal expense less than or equal to ₹1,000 → Fully Approved
- Meal expense greater than ₹1,000 → Approve up to ₹1,000 and reject the remaining amount

**Example**

| Claimed | Approved | Rejected |
|---------:|---------:|---------:|
| ₹900 | ₹900 | ₹0 |
| ₹1,800 | ₹1,000 | ₹800 |

---

### 🚖 Taxi Reimbursement

**Policy Limit:** ₹5,000

**Rules**

- Taxi expense less than or equal to ₹5,000 → Fully Approved
- Taxi expense greater than ₹5,000 → Approve up to ₹5,000 and reject the remaining amount

**Example**

| Claimed | Approved | Rejected |
|---------:|---------:|---------:|
| ₹700 | ₹700 | ₹0 |
| ₹6,000 | ₹5,000 | ₹1,000 |

---

### ✈ Flight Reimbursement

Flight reimbursement depends on **both the flight type and the actual airfare claimed**.

#### Economy Class

- Entire airfare is reimbursable.
- The full flight fare is approved.

**Example**

| Flight Type | Flight Fare | Approved | Rejected |
|--------------|------------:|----------:|----------:|
| Economy | ₹15,000 | ₹15,000 | ₹0 |

#### Business Class

- Business class airfare is **not reimbursable** under the current company policy.
- The complete airfare is rejected.

**Example**

| Flight Type | Flight Fare | Approved | Rejected |
|--------------|------------:|----------:|----------:|
| Business | ₹25,000 | ₹0 | ₹25,000 |

> **Note:** The policy states that Business Class requires Director approval. In the current implementation, Business Class airfare is rejected directly. This can be extended in future versions to support Director approval workflows.

---

### 🛍 Shopping Expenses

Shopping is considered a personal expense.

**Rule**

- Shopping expenses are never reimbursable.
- The entire claimed amount is rejected.

---

## Receipt Validation Rules

Receipts are validated before processing the reimbursement.

### Valid Receipt

- Receipt exists in the receipt database
- Receipt attachment is available

Result:

- Continue reimbursement processing

---

### No Receipts Uploaded

If the employee submits a reimbursement claim containing reimbursable expenses but does not upload any receipts:

**Decision**

- Manual Review

Reason:

Supporting documents are mandatory for reimbursement.

---

### Receipt Not Found

If any referenced receipt ID does not exist in the system:

**Decision**

- Manual Review

Reason:

The submitted receipt cannot be verified.

---

### Missing Receipt Attachment

If a receipt exists but its supporting attachment is unavailable:

**Decision**

- Manual Review

Reason:

The expense cannot be verified without supporting proof.

---

## Duplicate Receipt Detection

If a receipt has already been used in another reimbursement claim:

**Decision**

- Reject

Reason:

Duplicate reimbursement claims are not permitted.

---

## Required Approver

The required approver is selected automatically based on the **total claimed reimbursement amount**.

| Total Claim Amount | Required Approver |
|-------------------:|------------------|
| Up to ₹10,000 | Manager |
| ₹10,001 – ₹50,000 | Senior Manager |
| Above ₹50,000 | Director |

---

## Final Decision Logic

After evaluating every expense and validating all supporting documents, the Business Decision Engine determines one of the following outcomes.

### ✅ Approve

The claim is fully approved when:

- All expenses comply with company policy.
- All receipts are valid.
- No duplicate receipts are found.

---

### 🟡 Partially Approved

The claim is partially approved when:

- Some expenses comply with company policy.
- Remaining expenses exceed reimbursement limits or are not reimbursable.

Only the eligible amount is approved.

---

### 🔴 Reject

The claim is rejected when:

- Duplicate receipts are detected.
- No reimbursable expenses remain after applying company policies.

---

### 🟠 Manual Review

The claim is sent for manual review when:

- No receipts are uploaded.
- Receipt attachment is missing.
- Receipt ID cannot be found.
- Supporting documents require human verification.

---

## Why a Business Decision Engine?

Financial calculations should always be deterministic.

Large Language Models are probabilistic and may generate inconsistent reimbursement calculations. Therefore, this project separates **business logic** from **AI-generated explanations**.

The Business Decision Engine is responsible for:

- Expense validation
- Policy enforcement
- Receipt verification
- Duplicate receipt detection
- Reimbursement calculation
- Approval authority determination
- Final reimbursement decision

Google Gemini is responsible only for:

- Generating a human-readable explanation
- Identifying relevant policy references
- Producing a confidence score

This architecture provides:

- ✅ Consistent financial decisions
- ✅ Explainable AI responses
- ✅ Auditability
- ✅ Reliable reimbursement calculations
- ✅ Clear separation between deterministic logic and AI reasoning
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
  "decision": "Approve",
  "approved_amount": 28300,
  "rejected_amount": 0,
  "approver": "Senior Manager",
  "expenses": [
    {
      "category": "Hotel",
      "claimed": 1500,
      "approved": 1500,
      "rejected": 0,
      "status": "Approved",
      "remarks": "Within limit"
    },
    {
      "category": "Meal",
      "claimed": 1000,
      "approved": 1000,
      "rejected": 0,
      "status": "Approved",
      "remarks": "Within limit"
    },
    {
      "category": "Taxi",
      "claimed": 800,
      "approved": 800,
      "rejected": 0,
      "status": "Approved",
      "remarks": "Within limit"
    },
    {
      "category": "Flight",
      "claimed": 25000,
      "approved": 25000,
      "rejected": 0,
      "status": "Approved",
      "remarks": "Economy airfare reimbursed."
    }
  ],
  "missing_documents": [],
  "policy_references": [
    "Hotel Policy",
    "Meal Policy",
    "Taxi Policy",
    "Flight Policy",
    "Shopping Policy"
  ],
  "confidence": 0.98,
  "explanation": "The hotel expense of ₹1500 was fully approved as it was within the maximum reimbursement limit of ₹7000 per night, as per the Hotel Expenses policy. The meal expense of ₹1000 was fully approved, aligning with the maximum daily reimbursement limit of ₹1000 per day under the Meal Expenses policy. The taxi expense of ₹800 was fully approved as it was within the maximum reimbursement limit of ₹5000, as per the Taxi Expenses policy. The flight fare of ₹25000 for an Economy class ticket was fully approved, consistent with the Flight Expenses policy which reimburses Economy class travel. No missing receipts were identified for this claim."
}
```

---

# 🔑 Environment Variables

Before running the application, create a `.env` file in the project root directory and add your Google Gemini API key.

Example:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Replace `your_google_api_key_here` with your actual Google Gemini API key.

> **Note:** The application uses this environment variable to authenticate requests to the Google Gemini API.


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

## Run Streamlit

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
