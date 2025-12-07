
# 📘 AI-Powered RFP Management System

An end-to-end platform that automates vendor outreach, email tracking, proposal extraction, and structured pricing analysis using **OCR** and the **Gemini AI** model.

---

## 1. Project Setup

### 1.a Prerequisites

Before running the system, ensure the following components are installed:

#### **Backend Requirements**

* **Python 3.10+** (recommended python 3.11.0)
* **PostgreSQL 15**
* **Tesseract OCR:** Used for optical character recognition.
    * *Windows Users:* Install from the UB Mannheim build: [https://github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki)
* **Poppler:** Required for converting PDF documents to images.
    * *Windows Users:* Download from: [https://github.com/oschwartz10612/poppler-windows/releases/](https://github.com/oschwartz10612/poppler-windows/releases/)

#### **Frontend Requirements**

* **Node.js 18+**
* **npm / yarn / pnpm** (Node package manager)

---

### 1.b API Keys and Environment Configuration

Create a file named **`.env`** inside the `/backend` directory and populate it with your configuration details, especially the API and email credentials.

```dotenv
DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:5433/rfp_db"

# Email Configuration (Requires Gmail App Password)
EMAIL_FROM="your-email@gmail.com"
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASS=your-app-password
IMAP_HOST=imap.gmail.com

# AI Provider Configuration
LLM_PROVIDER="gemini"
GEMINI_API_KEY="your-key-here"

# Optional/Fallback Keys
OPENAI_API_KEY="your-key-here"
GROQ_API_KEY="your-key-here"
````

-----

### 1.c Installation Steps

#### **Backend Setup**

Navigate to the backend directory and install dependencies, then set up the database schema.

```bash
cd backend
pip install -r requirements.txt
prisma generate
prisma migrate deploy
# OR: prisma db push (for development environment)
```

#### **Frontend Setup**

Navigate to the frontend directory and install dependencies, then start the development server.

```bash
cd frontend
npm install
npm run dev
```

-----

### 1.d Configure Email Sending & Receiving

This system uses **IMAP** to receive vendor replies and **SMTP** to send initial RFPs. Authentication requires a Gmail **App Password** as Google has phased out support for "Less Secure Apps."

#### **1. Enable IMAP in Gmail**

1.  Open the Gmail **Forwarding and POP/IMAP** settings page: $\rightarrow$ [https://mail.google.com/mail/u/0/\#settings/fwdandpop](https://mail.google.com/mail/u/0/#settings/fwdandpop)
2.  Scroll to the **IMAP Access** section.
3.  Select **Enable IMAP**.
4.  Click **Save Changes**.

#### **2. Generate Gmail App Password**

1.  Enable **2-Step Verification** on your Google Account (this is mandatory).
2.  Go to the **App Passwords** page: $\rightarrow$ [https://myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)
3.  Select app type: **Mail**
4.  Select device: **Other** $\rightarrow$ Enter: **RFP System**
5.  Google will provide a 16-character app password.
6.  Copy this password and use it to set `SMTP_PASS` (which handles both SMTP and IMAP authentication) in the `.env` file. **Do not use your main Gmail password.**

-----

### 1.e Running Everything Locally

#### **Start PostgreSQL (Recommended: Docker)**

Use Docker Compose from inside the `backend` folder:

```bash
cd backend
docker compose up -d
```

#### **Start PostgreSQL (Manual Docker Run)**

```bash
docker run -d --name rfp_postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=rfp_db \
  -p 5433:5432 postgres:15
```

#### **Start Backend and Frontend**

1.  **Backend (API Server):**
    ```bash
    cd backend
    uvicorn app.main:app --reload
    ```
2.  **Frontend (Web Interface):**
    ```bash
    cd frontend
    npm run dev
    ```

#### **Background Email Sync Loop**

The backend automatically polls the IMAP inbox every **15 seconds** to extract replies, identify vendors via **Ref-ID**, log the email, and process proposals/attachments.

To manually trigger a sync check, use the endpoint:
`GET /email/receive`

-----

## 2\. Tech Stack Overview

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | React + Vite, TypeScript, TailwindCSS, Material UI, Axios | Modern, fast web interface for user interaction. |
| **Backend** | **FastAPI**, **Prisma Client Python**, PostgreSQL, `asyncio` | High-performance async API with a robust ORM and relational database. |
| **AI/OCR** | **Google Gemini 2.5 Flash**, Tesseract, Poppler, `pdf2image` | Core intelligence for proposal extraction and file processing. |
| **Email** | **SMTP** (outgoing), **IMAP** (incoming) | Standard protocols for reliable email communication and tracking. |

### Key Libraries

  * `pdf2image`, `pytesseract`: For the OCR pipeline.
  * `google-generativeai`: To interact with the Gemini API.
  * `prisma-client-py`: The ORM for PostgreSQL.
  * `fastapi`, `uvicorn`: The web framework and server.

-----

## 3\. API Documentation

The full documentation is available at the `/docs` route when the backend is running.

### 3.a Main Endpoints

| Category | Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **RFP** | `POST` | `/rfp/create` | Creates a new Request for Proposal. |
| | `GET` | `/rfp/user/{userId}` | Lists all RFPs for a specific user. |
| **Vendors** | `POST` | `/vendor/create` | Adds a new vendor to the system. |
| | `GET` | `/vendor/all` | Lists all registered vendors. |
| **Sending** | `POST` | `/rfp/send` | Generates **Ref-ID** and sends the RFP email to vendors. |
| **Email Sync** | `GET` | `/email/receive` | Triggers a manual IMAP email sync check. Returns received/saved count. |
| | `GET` | `/email/logs` | Retrieves all email logs. |
| | `GET` | `/email/logs/{rfpVendorId}` | Retrieves logs specific to an RFP-Vendor relationship. |
| **Proposals** | `GET` | `/proposal/{rfpVendorId}` | Gets extracted proposals for a vendor on a specific RFP. |
| | `POST` | `/proposal/create` | Manually creates or updates a proposal record. |

-----

## 4\. Decisions & Assumptions

### 4.a Key Design Decisions

1.  **Email-Based Workflow:** The system centers around vendor email replies. This is the primary mechanism for **tracking communication** and triggering **proposal extraction**.
2.  **Unique Ref-ID Mapping:** A unique `Ref-ID` is generated and included in every outgoing RFP email. This UUID is critical for reliably mapping an incoming vendor reply back to the correct `RFPVendor` record.
3.  **AI-Assisted Extraction:** **Gemini 2.5 Flash** is used for sophisticated extraction of structured data (pricing, items, warranty, etc.) from raw email text and attachments, with a regex-based parser as a **fallback**.
4.  **Asynchronous Processing:** Email sync, PDF conversion, and OCR/AI processing are run **asynchronously** using `asyncio` background tasks to prevent blocking the main API thread.

### 4.b Assumptions

  * Vendors reply to the email **with the Ref-ID present** in the subject or body.
  * Proposal content may be in the **email body** or attached as a **PDF/image** (JPEG/PNG).
  * Robust **OCR error handling** and AI output schema enforcement are necessary to handle low-quality images and broken JSON responses.
  * The system includes logic for **deduplication** to avoid repeated processing of the same email and proposal.

