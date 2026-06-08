<div align="center">

# AI Knowledge Base API

### A Production-Ready Retrieval-Augmented Generation (RAG) API

[![Python 3.12+](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=for-the-badge)](LICENSE)

Upload documents. Ask questions. Get intelligent, context-aware answers powered by OpenAI's GPT models with full source attribution.

[**Getting Started**](#-getting-started) |
[**API Docs**](#-api-reference) |
[**Architecture**](#-architecture)

</div>

---

## Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Database Setup](#database-setup)
  - [Running the Server](#running-the-server)
- [Docker Deployment](#-docker-deployment)
- [API Reference](#-api-reference)
  - [Authentication](#authentication)
  - [Documents](#documents)
  - [Chat](#chat)
  - [Health](#health)
- [RAG Pipeline Deep Dive](#-rag-pipeline-deep-dive)
- [Database Schema](#-database-schema)
- [Usage Examples](#-usage-examples)
- [Cloud Deployment](#-cloud-deployment)
- [Troubleshooting](#-troubleshooting)
- [Contributing](#-contributing)
- [License](#-license)

---

## Features

<div align="center">

| Feature | Description |
|:---|:---|
| **Document Ingestion** | Upload `.pdf`, `.docx`, `.txt`, `.md`, `.html`, and `.json` files. Documents are automatically partitioned, chunked, embedded, and stored in a vector database. |
| **Intelligent Chat** | Ask questions about your documents and receive accurate, context-grounded answers with relevance scoring and source attribution. |
| **Multi-turn Conversations** | Session-based chat with full history tracking -- the AI remembers prior context within a conversation. |
| **User Authentication** | Secure JWT-based auth with access tokens, refresh tokens, and Argon2 password hashing. |
| **Cost & Usage Tracking** | Per-message and per-session token usage with estimated cost metrics for budget management. |
| **Document Enrichment** | Automatic table summarization and image description during ingestion for richer, more accurate search results. |
| **Embedding Cache** | SHA256-based caching layer that reduces redundant OpenAI API calls and optimizes costs. |
| **Full-Text Semantic Search** | ChromaDB-powered similarity search retrieves the most relevant document chunks for each query. |
| **Auto Session Naming** | Chat sessions are automatically titled and described based on conversation content. |

</div>

### Feature Highlights

<details>
<summary><b>Document Ingestion Pipeline</b> (click to expand)</summary>

<br>

Upload any supported document and the system automatically:
1. Extracts text, tables, and images using Unstructured's HI_RES strategy
2. Enriches tables with AI-generated summaries and images with descriptions
3. Splits content into semantic chunks with configurable size and overlap
4. Generates embeddings via OpenAI with an intelligent caching layer
5. Stores vectors in ChromaDB for lightning-fast similarity search

</details>

<details>
<summary><b>Intelligent Chat with Source Attribution</b> (click to expand)</summary>

<br>

Every AI response includes:
- Context-grounded answers based on your uploaded documents
- Relevance scores for each retrieved chunk
- Token usage breakdown (input/output)
- Estimated cost per message
- Full conversation history within the session

</details>

<details>
<summary><b>JWT Authentication Flow</b> (click to expand)</summary>

<br>

- **Register** with name, email, and password (Argon2 hashed)
- **Login** to receive access token (60 min) + refresh token (7 days)
- **Refresh** expired access tokens without re-authenticating
- **Revoke** individual tokens or **logout** to revoke all tokens

</details>

---

## Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|:---|:---|:---|
| **Web Framework** | ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) | High-performance async API framework |
| **ASGI Server** | ![Uvicorn](https://img.shields.io/badge/Uvicorn-2F4F4F?style=flat-square) | Lightning-fast ASGI server |
| **Database** | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white) | Relational data storage |
| **ORM** | ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy_2.0-D71F00?style=flat-square) | Database abstraction layer |
| **Migrations** | ![Alembic](https://img.shields.io/badge/Alembic-6BA81E?style=flat-square) | Schema version control |
| **Vector Store** | ![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6F00?style=flat-square) | Persistent vector database |
| **LLM** | ![OpenAI](https://img.shields.io/badge/OpenAI_GPT-412991?style=flat-square&logo=openai&logoColor=white) | Language model via LangChain |
| **Embeddings** | ![OpenAI](https://img.shields.io/badge/text--embedding--3--small-412991?style=flat-square&logo=openai&logoColor=white) | Vector embedding generation |
| **Doc Parsing** | ![Unstructured](https://img.shields.io/badge/Unstructured-000000?style=flat-square) | HI_RES document partitioning |
| **Auth** | ![JWT](https://img.shields.io/badge/JWT+Argon2-000000?style=flat-square&logo=jsonwebtokens&logoColor=white) | Token-based authentication |
| **Containerization** | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) | Container deployment |

</div>

---

## Architecture

### High-Level System Architecture

```
                                    AI Knowledge Base API
                                    =====================

    +-----------+         +-------------------+         +------------------+
    |           |  HTTP   |                   |         |                  |
    |  Client   +-------->+   FastAPI Server  +-------->+   MySQL (SQL)    |
    | (Browser/ |         |                   |         |   - Users        |
    |  Postman/ |         |  +-------------+  |         |   - Documents    |
    |  Frontend)|         |  | Auth Layer  |  |         |   - Sessions     |
    |           |         |  | (JWT+Argon2)|  |         |   - Messages     |
    +-----------+         |  +-------------+  |         |   - Cache        |
                          |                   |         +------------------+
                          |  +-------------+  |
                          |  | RAG Engine  |  |         +------------------+
                          |  |             +----------->+                  |
                          |  | - Partition |  |         |   ChromaDB       |
                          |  | - Enrich   |  |         |   (Vectors)      |
                          |  | - Chunk    |  |         |                  |
                          |  | - Embed    |  |         +------------------+
                          |  | - Retrieve |  |
                          |  +------+------+  |         +------------------+
                          |         |         |         |                  |
                          |         +-------------------+   OpenAI API     |
                          |                   |         |   - GPT (Chat)   |
                          +-------------------+         |   - Embeddings   |
                                                        |   - Vision       |
                                                        +------------------+
```

### RAG Pipeline Architecture

```
   DOCUMENT INGESTION                              QUERY TIME
   ==================                              ==========

   +----------+     +-------------+                +----------+
   | Document |     |  Partition  |                |  User    |
   | Upload   +---->+  (Unstruct- |                |  Query   |
   | (.pdf,   |     |   ured)     |                +----+-----+
   |  .docx,  |     +------+------+                     |
   |  .txt,   |            |                             v
   |  .md,    |     +------v------+                +-----+------+
   |  .html,  |     |   Enrich    |                |  Embed     |
   |  .json)  |     | - Table     |                |  Query     |
   +----------+     |   summaries |                +-----+------+
                    | - Image     |                      |
                    |   descriptions                     v
                    +------+------+                +-----+------+
                           |                       |  Semantic  |
                    +------v------+                |  Search    |
                    |   Chunk     |                |  (Top-K)   |
                    | - Recursive |                +-----+------+
                    |   splitter  |                      |
                    | - 3000 tok  |                      v
                    | - 200 over- |                +-----+------+
                    |   lap       |                |  Build     |
                    +------+------+                |  Context   |
                           |                       +-----+------+
                    +------v------+                      |
                    |   Embed     |                      v
                    | - OpenAI    |                +-----+------+     +-----------+
                    | - Cache     |                |  LLM Call  +---->+ AI        |
                    +------+------+                | (GPT +     |     | Response  |
                           |                       |  History + |     | + Sources |
                    +------v------+                |  Context)  |     +-----------+
                    |   Store     |                +------------+
                    | (ChromaDB)  |
                    +-------------+
```

### Authentication Flow

```
   REGISTER                    LOGIN                      PROTECTED REQUEST
   ========                    =====                      =================

   +--------+                  +--------+                  +--------+
   | Client |                  | Client |                  | Client |
   +---+----+                  +---+----+                  +---+----+
       |                           |                           |
       | POST /auth/register       | POST /auth/login          | GET /documents
       | {name, email, password}   | {email, password}         | Authorization: Bearer <token>
       |                           |                           |
       v                           v                           v
   +---+----+                  +---+----+                  +---+----+
   | Hash   |                  | Verify |                  | Decode |
   | Pass   |                  | Pass   |                  | JWT    |
   | Argon2 |                  | Argon2 |                  | HS256  |
   +---+----+                  +---+----+                  +---+----+
       |                           |                           |
       v                           v                           |
   +---+----+                  +---+----+                  +---+----+
   | Store  |                  | Issue  |                  | Load   |
   | User   |                  | Tokens |                  | User   |
   | in DB  |                  +---+----+                  +---+----+
   +---+----+                      |                           |
       |                           v                           v
       v                      Access Token (60m)          Process Request
   201 Created                Refresh Token (7d)          Return Response
```

---

## Project Structure

```
ai-knowledgebase-api/
│
├── app/                              # Application source code
│   ├── __init__.py
│   ├── main.py                       # FastAPI app entry point, CORS, routes
│   │
│   ├── ai/                           # AI & RAG components
│   │   └── rag/
│   │       ├── __init__.py
│   │       ├── ingestion.py          # Orchestrates the full ingestion pipeline
│   │       ├── doc_partition.py      # Document extraction (Unstructured HI_RES)
│   │       ├── enhance_content.py    # Table summarization & image descriptions
│   │       ├── chunker.py           # Text splitting (recursive + title-based)
│   │       ├── embedder.py          # OpenAI embedding generation + caching
│   │       ├── vector_store.py      # ChromaDB vector storage & management
│   │       └── retrieval.py         # Semantic search & LLM chat invocation
│   │
│   ├── api/                          # API layer
│   │   ├── __init__.py
│   │   ├── router.py                 # Main API router (prefix: /api/v1)
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── auth.py              # Auth endpoints (register, login, refresh, logout)
│   │       ├── chat.py              # Chat endpoints (send message, history, sessions)
│   │       └── document.py          # Document endpoints (upload, list, download, delete)
│   │
│   ├── core/                         # Core utilities & config
│   │   ├── __init__.py
│   │   ├── config.py                # Environment variable configuration
│   │   ├── security.py              # JWT creation/verification, password hashing
│   │   ├── dependencies.py          # FastAPI dependency injection
│   │   ├── exceptions.py            # Custom exception classes & handlers
│   │   └── logger.py               # Logging configuration
│   │
│   ├── db/                           # Database layer
│   │   ├── __init__.py
│   │   ├── database.py              # SQLAlchemy engine & session factory
│   │   ├── create_tables.py         # Table creation utility
│   │   └── models/                  # SQLAlchemy ORM models
│   │       ├── __init__.py
│   │       ├── base.py             # Declarative base
│   │       ├── user.py             # User model
│   │       ├── document.py         # Document & DocumentChunk models
│   │       ├── chat.py             # ChatSession & Message models
│   │       ├── refresh_token.py    # RefreshToken model
│   │       ├── cache.py            # EmbeddingCache model
│   │       ├── enums.py            # DocumentSource & MessageRole enums
│   │       ├── api_logs.py         # API logging model
│   │       └── events.py           # Event tracking model
│   │
│   ├── modules/                      # Business logic / service layer
│   │   ├── __init__.py
│   │   ├── auth_service.py          # Authentication business logic
│   │   ├── chat_service.py          # Chat & session management logic
│   │   ├── document_service.py      # Document processing & management
│   │   └── user_service.py          # User management
│   │
│   └── schemas/                      # Pydantic request/response schemas
│       ├── __init__.py
│       ├── user.py                  # User creation & response schemas
│       ├── chat.py                  # Chat message & session schemas
│       ├── document.py              # Document upload & response schemas
│       └── refresh_token.py         # Token schemas
│
├── alembic/                          # Database migrations
│   ├── env.py                        # Migration environment config
│   ├── script.py.mako                # Migration template
│   └── versions/                     # Migration version files
│
├── chroma_db/                        # ChromaDB persistent storage (auto-created)
├── uploaded_doc_files/               # Uploaded document storage (auto-created)
│
├── .env                              # Environment variables (not in git)
├── .gitignore                        # Git ignore rules
├── .python-version                   # Python version specification
├── alembic.ini                       # Alembic configuration
├── Dockerfile                        # Docker build configuration
├── Procfile                          # Heroku deployment config
├── pyproject.toml                    # Project metadata (uv/pip)
├── railway.toml                      # Railway deployment config
├── requirements.txt                  # Python dependencies
└── README.md                         # This file
```

---

## Getting Started

### Prerequisites

| Requirement | Version | Purpose |
|:---|:---|:---|
| **Python** | 3.12+ | Runtime |
| **MySQL** | 8.0+ | Relational database |
| **Tesseract OCR** | Latest | PDF/image text extraction |
| **Poppler** | Latest | PDF rendering |
| **ImageMagick** | Latest | Image processing |
| **OpenAI API Key** | -- | LLM & embeddings |

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/your-username/ai-knowledgebase-api.git
cd ai-knowledgebase-api
```

#### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

**Activate the virtual environment:**

| OS | Command |
|:---|:---|
| **macOS / Linux** | `source .venv/bin/activate` |
| **Windows (CMD)** | `.venv\Scripts\activate` |
| **Windows (PowerShell)** | `.venv\Scripts\Activate.ps1` |

#### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 4. Install System Dependencies

<details>
<summary><b>macOS (Homebrew)</b></summary>

```bash
brew install tesseract poppler imagemagick
```
</details>

<details>
<summary><b>Ubuntu / Debian</b></summary>

```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr poppler-utils libmagickwand-dev
```
</details>

<details>
<summary><b>Windows</b></summary>

1. **Tesseract**: Download from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH
2. **Poppler**: Download from [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases) and add to PATH
3. **ImageMagick**: Download from [imagemagick.org](https://imagemagick.org/script/download.php)
</details>

### Environment Variables

Create a `.env` file in the project root:

```env
# =============================================
# DATABASE CONFIGURATION
# =============================================
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_secure_password
MYSQL_DATABASE=ai_knowledge_base_db

# =============================================
# OPENAI CONFIGURATION
# =============================================
OPENAI_API_KEY=sk-your-openai-api-key-here

# =============================================
# AUTHENTICATION
# =============================================
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# =============================================
# RAG PIPELINE SETTINGS
# =============================================
CHUNK_SIZE=3000                          # Characters per chunk
CHUNK_OVERLAP=200                        # Overlap between chunks
EMBEDDING_MODEL=text-embedding-3-small   # OpenAI embedding model
LARGE_LANGUAGE_MODEL=gpt-4o-mini         # LLM for chat responses
MAX_TOKENS=4096                          # Max tokens per LLM response

# =============================================
# STORAGE DIRECTORIES
# =============================================
UPLOADED_FILES_DIR=uploaded_doc_files     # Document storage path
CHROMA_PERSISTENCE_DIR=chroma_db         # Vector DB storage path

# =============================================
# COST TRACKING
# =============================================
INPUT_COST_PER_MILLION=0.15              # Cost per 1M input tokens
OUTPUT_COST_PER_MILLION=0.60             # Cost per 1M output tokens

# =============================================
# APPLICATION INFO
# =============================================
AI_NAME=SonicAI                          # AI assistant name
COMPANY_NAME=Your Company Name
COMPANY_EMAIL=info@example.com
COMPANY_WEBSITE=https://example.com

# =============================================
# RATE LIMITING
# =============================================
API_RATE_LIMIT_PER_MINUTE=60
```

> **Warning**: Never commit your `.env` file to version control. It is already included in `.gitignore`.

### Database Setup

**1. Create the MySQL database:**

```sql
CREATE DATABASE ai_knowledge_base_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

**2. Run Alembic migrations:**

```bash
alembic upgrade head
```

### Running the Server

**Development mode (with hot reload):**

```bash
uvicorn app.main:app --reload
```

**Production mode:**

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Once running, access:

| Resource | URL |
|:---|:---|
| **API Base** | `http://localhost:8000` |
| **Swagger UI (Interactive Docs)** | `http://localhost:8000/docs` |
| **ReDoc (Alternative Docs)** | `http://localhost:8000/redoc` |
| **Health Check** | `http://localhost:8000/health` |

---

## Docker Deployment

### Build and Run

```bash
# Build the Docker image
docker build -t ai-knowledgebase-api .

# Run the container
docker run -p 8000:8000 --env-file .env ai-knowledgebase-api
```

### Docker Compose (with MySQL)

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db
    volumes:
      - uploaded_files:/app/uploaded_doc_files
      - chroma_data:/app/chroma_db

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
  uploaded_files:
  chroma_data:
```

```bash
docker-compose up -d
```

> **Note**: The Docker image includes all system dependencies (Tesseract, Poppler, ImageMagick) out of the box.

---

## API Reference

All endpoints are prefixed with `/api/v1`. Authentication is required for document and chat endpoints via Bearer token.

### Authentication

<details>
<summary><b>POST</b> <code>/api/v1/auth/register</code> -- Register a new user</summary>

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john@example.com",
  "is_active": true,
  "created_at": "2026-06-08T10:30:00Z"
}
```
</details>

<details>
<summary><b>POST</b> <code>/api/v1/auth/login</code> -- Login and receive tokens</summary>

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "dGhpcyBpcyBhIHJlZnJl...",
  "token_type": "bearer"
}
```
</details>

<details>
<summary><b>POST</b> <code>/api/v1/auth/refresh</code> -- Refresh an access token</summary>

**Request Body:**
```json
{
  "refresh_token": "dGhpcyBpcyBhIHJlZnJl..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "bmV3IHJlZnJlc2ggdG9r...",
  "token_type": "bearer"
}
```
</details>

<details>
<summary><b>POST</b> <code>/api/v1/auth/revoke</code> -- Revoke a refresh token</summary>

**Request Body:**
```json
{
  "refresh_token": "dGhpcyBpcyBhIHJlZnJl..."
}
```

**Response (200):**
```json
{
  "message": "Token revoked successfully"
}
```
</details>

<details>
<summary><b>POST</b> <code>/api/v1/auth/logout</code> -- Logout (revoke all tokens)</summary>

**Headers:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
{
  "message": "Successfully logged out"
}
```
</details>

---

### Documents

<details>
<summary><b>POST</b> <code>/api/v1/documents</code> -- Upload and process a document</summary>

**Headers:** `Authorization: Bearer <access_token>`
**Content-Type:** `multipart/form-data`

**Form Fields:**

| Field | Type | Required | Description |
|:---|:---|:---|:---|
| `file` | File | Yes | The document file (.pdf, .docx, .txt, .md, .html, .json) |
| `description` | String | No | Description of the document |
| `source` | String | No | Source type: `uploaded`, `imported`, `generated`, `scraped` |
| `tags` | JSON | No | List of tags for categorization |

**Response (201):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "name": "company-handbook.pdf",
  "file_type": ".pdf",
  "size_bytes": 2458624,
  "chunks": 45,
  "tokens": 32000,
  "total_tables": 3,
  "total_images": 7,
  "is_processed": true,
  "created_at": "2026-06-08T10:35:00Z"
}
```
</details>

<details>
<summary><b>GET</b> <code>/api/v1/documents</code> -- List all documents (paginated)</summary>

**Headers:** `Authorization: Bearer <access_token>`

**Query Parameters:**

| Parameter | Type | Default | Description |
|:---|:---|:---|:---|
| `skip` | int | 0 | Number of records to skip |
| `limit` | int | 10 | Number of records to return |

**Response (200):**
```json
[
  {
    "id": "660e8400-e29b-41d4-a716-446655440001",
    "name": "company-handbook.pdf",
    "file_type": ".pdf",
    "size_bytes": 2458624,
    "chunks": 45,
    "is_processed": true,
    "created_at": "2026-06-08T10:35:00Z"
  }
]
```
</details>

<details>
<summary><b>GET</b> <code>/api/v1/documents/{id}</code> -- Get document details</summary>

**Headers:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
{
  "id": "660e8400-e29b-41d4-a716-446655440001",
  "name": "company-handbook.pdf",
  "description": "Employee handbook 2026",
  "file_type": ".pdf",
  "size_bytes": 2458624,
  "source": "uploaded",
  "tags": ["hr", "policies"],
  "chunks": 45,
  "tokens": 32000,
  "total_tables": 3,
  "total_images": 7,
  "chunk_ids": ["660e...001_chunk_0", "660e...001_chunk_1", "..."],
  "is_processed": true,
  "created_at": "2026-06-08T10:35:00Z"
}
```
</details>

<details>
<summary><b>GET</b> <code>/api/v1/documents/{id}/download</code> -- Download a document file</summary>

**Headers:** `Authorization: Bearer <access_token>`

**Response:** Binary file download with appropriate Content-Type header.
</details>

<details>
<summary><b>DELETE</b> <code>/api/v1/documents/{id}</code> -- Delete a document</summary>

**Headers:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
{
  "message": "Document deleted successfully"
}
```

> Deleting a document also removes all associated chunks from both MySQL and ChromaDB.
</details>

---

### Chat

<details>
<summary><b>POST</b> <code>/api/v1/chat</code> -- Send a message and get an AI response</summary>

**Headers:** `Authorization: Bearer <access_token>`

**Request Body:**
```json
{
  "message": "What is the company's vacation policy?",
  "session_id": null,
  "document_ids": ["660e8400-e29b-41d4-a716-446655440001"]
}
```

> Set `session_id` to `null` for a new conversation, or provide an existing session ID to continue a conversation.

**Response (200):**
```json
{
  "session_id": "770e8400-e29b-41d4-a716-446655440002",
  "message": {
    "id": "880e8400-e29b-41d4-a716-446655440003",
    "role": "assistant",
    "content": "Based on the company handbook, the vacation policy states that...",
    "document_ids_used": ["660e8400-e29b-41d4-a716-446655440001"],
    "relevance_scores": [0.92, 0.87, 0.85],
    "retrieved_chunk_count": 3,
    "input_tokens": 1250,
    "output_tokens": 340,
    "estimated_cost": 0.000391,
    "created_at": "2026-06-08T10:40:00Z"
  }
}
```
</details>

<details>
<summary><b>GET</b> <code>/api/v1/chat/{session_id}/history</code> -- Get chat history</summary>

**Headers:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
{
  "session_id": "770e8400-e29b-41d4-a716-446655440002",
  "session_name": "Vacation Policy Questions",
  "messages": [
    {
      "id": "...",
      "role": "user",
      "content": "What is the company's vacation policy?",
      "created_at": "2026-06-08T10:40:00Z"
    },
    {
      "id": "...",
      "role": "assistant",
      "content": "Based on the company handbook...",
      "input_tokens": 1250,
      "output_tokens": 340,
      "estimated_cost": 0.000391,
      "created_at": "2026-06-08T10:40:01Z"
    }
  ],
  "total_messages": 2,
  "total_tokens": 1590,
  "total_cost": 0.000391
}
```
</details>

<details>
<summary><b>GET</b> <code>/api/v1/chat/sessions</code> -- List all chat sessions</summary>

**Headers:** `Authorization: Bearer <access_token>`

**Response (200):**
```json
[
  {
    "id": "770e8400-e29b-41d4-a716-446655440002",
    "name": "Vacation Policy Questions",
    "description": "Discussion about company vacation policies and PTO",
    "total_messages": 6,
    "total_tokens": 8450,
    "total_cost": 0.002105,
    "is_active": true,
    "created_at": "2026-06-08T10:40:00Z"
  }
]
```
</details>

<details>
<summary><b>GET</b> <code>/api/v1/chat/sessions/user/{user_id}</code> -- List sessions for a user</summary>

**Headers:** `Authorization: Bearer <access_token>`

**Response:** Same format as "List all chat sessions" above, filtered by user.
</details>

---

### Health

| Method | Endpoint | Description | Auth Required |
|:---|:---|:---|:---|
| `GET` | `/` | Returns welcome message | No |
| `GET` | `/health` | Health check | No |

---

## RAG Pipeline Deep Dive

### Stage 1: Document Partitioning

```python
# Powered by Unstructured (HI_RES strategy)
# Extracts: text blocks, tables, images with page metadata
```

| File Type | Extraction Method |
|:---|:---|
| `.pdf` | OCR + layout analysis (Tesseract + Poppler) |
| `.docx` | XML parsing with structure preservation |
| `.txt` | Direct text ingestion |
| `.md` | Markdown parsing |
| `.html` | HTML parsing with tag removal |
| `.json` | JSON structure flattening |

### Stage 2: Content Enrichment

The enrichment stage uses OpenAI to enhance extracted content:

- **Tables**: Each table is sent to GPT with a prompt to generate a concise, searchable summary
- **Images**: Each image is sent to GPT-4 Vision to generate descriptive text

This enrichment significantly improves retrieval accuracy for queries about tabular data or visual content.

### Stage 3: Chunking Strategy

```
┌──────────────────────────────────────────────────┐
│              Original Document Text               │
│                  (e.g., 15,000 chars)             │
└──────────────────┬───────────────────────────────┘
                   │
         RecursiveCharacterTextSplitter
         chunk_size=3000, overlap=200
                   │
    ┌──────────────┼──────────────┐
    │              │              │
    v              v              v
┌────────┐   ┌────────┐   ┌────────┐
│Chunk 1 │   │Chunk 2 │   │Chunk 3 │
│3000 ch │   │3000 ch │   │2400 ch │
│        │   │        │   │        │
│   ┌────┤   ├────┐   │   │        │
│   │overlap│ │overlap│   │        │
│   │ 200  │ │ 200 │  │   │        │
└───┴────┘   └────┴───┘   └────────┘
```

The splitter uses these separators (in order): `\n\n` > `\n` > `. ` > ` ` > `""`

### Stage 4: Embedding & Caching

```
              Text Chunk
                  │
                  v
          ┌───────────────┐
          │  SHA256 Hash   │
          └───────┬───────┘
                  │
          ┌───────v───────┐
          │ Cache Lookup   │
          └───────┬───────┘
                  │
         ┌────────┴────────┐
         │                 │
    Cache HIT         Cache MISS
         │                 │
         v                 v
   Return cached     ┌──────────┐
   embedding         │ OpenAI   │
                     │ API Call │
                     └────┬─────┘
                          │
                     Save to cache
                          │
                     Return embedding
```

### Stage 5: Vector Storage (ChromaDB)

Each chunk is stored with rich metadata:

```json
{
  "id": "document-uuid_chunk_0",
  "embedding": [0.0123, -0.0456, ...],
  "metadata": {
    "document_id": "document-uuid",
    "filename": "handbook.pdf",
    "source": "uploaded",
    "upload_date": "2026-06-08",
    "file_type": ".pdf",
    "tags": ["hr", "policies"],
    "chunk_index": 0
  },
  "document": "The actual chunk text content..."
}
```

### Query-Time Retrieval

1. User query is embedded using the same model
2. ChromaDB performs cosine similarity search (Top-K, default K=10)
3. Results can be filtered by specific `document_ids`
4. Retrieved chunks are enriched with relevance scores
5. Context is built with chunks + conversation history (last 20 messages)
6. Full context passed to LLM for response generation

---

## Database Schema

### Entity Relationship Diagram

```
┌──────────────────┐       ┌──────────────────────┐       ┌──────────────────┐
│      User        │       │     ChatSession       │       │     Document     │
├──────────────────┤       ├──────────────────────┤       ├──────────────────┤
│ id (UUID, PK)    │       │ id (UUID, PK)         │       │ id (UUID, PK)    │
│ name             │       │ name                  │       │ name             │
│ email (unique)   │       │ description           │       │ file_location    │
│ password_hash    │  1:N  │ user_id (FK) ─────────┤       │ description      │
│ is_active        │◄──────┤ document_ids (JSON)   │       │ content          │
│ created_at       │       │ total_messages        │       │ file_type        │
│ updated_at       │       │ total_tokens          │       │ size_bytes       │
└────────┬─────────┘       │ total_cost            │       │ source (enum)    │
         │                 │ is_active             │       │ tags (JSON)      │
         │                 │ archived_at           │       │ chunks           │
         │                 │ created_at            │       │ tokens           │
         │                 │ updated_at            │       │ total_tables     │
         │                 └──────────┬────────────┘       │ total_images     │
         │                            │                    │ chunk_ids (JSON) │
         │                       1:N  │                    │ is_processed     │
         │                            │                    │ relevance_score  │
         │                 ┌──────────v────────────┐       │ created_at       │
         │                 │      Message          │       │ updated_at       │
         │                 ├──────────────────────┤       └────────┬─────────┘
         │                 │ id (UUID, PK)         │               │
         │                 │ session_id (FK) ──────┘               │
         │                 │ document_id (FK) ─────────────────────┘
         │                 │ role (enum)           │
         │                 │ content               │       ┌──────────────────┐
         │                 │ document_ids_used     │       │  DocumentChunk   │
         │                 │ relevance_scores      │       ├──────────────────┤
         │                 │ retrieved_chunk_count │       │ id (UUID, PK)    │
         │                 │ input_tokens          │       │ document_id (FK) │
         │                 │ output_tokens         │  1:N  │ chunk_index      │
         │                 │ estimated_cost        │◄──────┤ content          │
         │                 │ user_rating (1-5)     │       │ tokens           │
         │                 │ feedback              │       │ vector_id (unique│
         │                 │ created_at            │       │ created_at       │
         │                 └──────────────────────┘       └──────────────────┘
         │
    1:N  │
         │                 ┌──────────────────────┐       ┌──────────────────┐
         │                 │    RefreshToken       │       │  EmbeddingCache  │
         │                 ├──────────────────────┤       ├──────────────────┤
         └────────────────►│ id (UUID, PK)         │       │ id (String, PK)  │
                           │ user_id (FK)          │       │ text_hash (uniq) │
                           │ token (unique)        │       │ text_snippet     │
                           │ expires_at            │       │ embedding (JSON) │
                           │ is_revoked            │       │ embedding_model  │
                           │ created_at            │       │ hit_count        │
                           └──────────────────────┘       │ created_at       │
                                                          │ last_accessed_at │
                                                          └──────────────────┘
```

### Enums

| Enum | Values |
|:---|:---|
| `DocumentSourceEnum` | `uploaded`, `imported`, `generated`, `scraped` |
| `MessageRoleEnum` | `user`, `assistant`, `system` |

---

## Usage Examples

### Using cURL

#### Register a New User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

#### Login

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "securepassword123"
  }'
```

#### Upload a Document

```bash
curl -X POST http://localhost:8000/api/v1/documents \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -F "file=@/path/to/document.pdf" \
  -F "description=Company employee handbook" \
  -F "tags=[\"hr\", \"policies\"]"
```

#### Ask a Question

```bash
# Start a new conversation
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is the vacation policy for full-time employees?",
    "document_ids": ["DOCUMENT_ID_HERE"]
  }'
```

```bash
# Continue an existing conversation
curl -X POST http://localhost:8000/api/v1/chat \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "How many sick days are included?",
    "session_id": "SESSION_ID_FROM_PREVIOUS_RESPONSE"
  }'
```

#### Get Chat History

```bash
curl -X GET http://localhost:8000/api/v1/chat/SESSION_ID/history \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Using Python (requests)

```python
import requests

BASE_URL = "http://localhost:8000/api/v1"

# Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123"
})

# Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "john@example.com",
    "password": "securepassword123"
})
tokens = response.json()
headers = {"Authorization": f"Bearer {tokens['access_token']}"}

# Upload a document
with open("document.pdf", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/documents",
        headers=headers,
        files={"file": f},
        data={"description": "Company handbook"}
    )
doc_id = response.json()["id"]

# Chat with your documents
response = requests.post(f"{BASE_URL}/chat", headers=headers, json={
    "message": "Summarize the key policies in this document",
    "document_ids": [doc_id]
})
print(response.json()["message"]["content"])
```

### Using JavaScript (fetch)

```javascript
const BASE_URL = "http://localhost:8000/api/v1";

// Login
const loginRes = await fetch(`${BASE_URL}/auth/login`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    email: "john@example.com",
    password: "securepassword123",
  }),
});
const { access_token } = await loginRes.json();

// Chat
const chatRes = await fetch(`${BASE_URL}/chat`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    Authorization: `Bearer ${access_token}`,
  },
  body: JSON.stringify({
    message: "What are the main topics covered in the uploaded documents?",
    document_ids: ["your-document-id"],
  }),
});
const data = await chatRes.json();
console.log(data.message.content);
```

---

## Cloud Deployment

### Railway

The project includes a `railway.toml` for one-click deployment:

1. Connect your GitHub repository to [Railway](https://railway.app)
2. Add a MySQL service
3. Set environment variables in the Railway dashboard
4. Deploy

### Heroku

The project includes a `Procfile`:

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Add MySQL addon
heroku addons:create jawsdb:kitefin

# Set environment variables
heroku config:set OPENAI_API_KEY=sk-...
heroku config:set SECRET_KEY=your-secret-key
# ... set all other required variables

# Deploy
git push heroku main
```

### Docker (Any Cloud Provider)

```bash
# Build and push to your container registry
docker build -t your-registry/ai-knowledgebase-api:latest .
docker push your-registry/ai-knowledgebase-api:latest
```

Compatible with AWS ECS, Google Cloud Run, Azure Container Instances, DigitalOcean App Platform, and more.

---

## Troubleshooting

<details>
<summary><b>Tesseract not found</b></summary>

```
TesseractNotFoundError: tesseract is not installed or not in PATH
```

**Solution:** Install Tesseract OCR:
- macOS: `brew install tesseract`
- Ubuntu: `sudo apt-get install tesseract-ocr`
- Windows: Download from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) and add to PATH
</details>

<details>
<summary><b>Poppler not found</b></summary>

```
PDFInfoNotInstalledError: Unable to get page count. Is poppler installed?
```

**Solution:** Install Poppler:
- macOS: `brew install poppler`
- Ubuntu: `sudo apt-get install poppler-utils`
- Windows: Download from [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases)
</details>

<details>
<summary><b>MySQL connection refused</b></summary>

```
sqlalchemy.exc.OperationalError: Can't connect to MySQL server
```

**Solution:**
1. Ensure MySQL is running: `mysql.server start` (macOS) or `sudo systemctl start mysql` (Linux)
2. Verify credentials in `.env`
3. Ensure the database exists: `CREATE DATABASE ai_knowledge_base_db;`
</details>

<details>
<summary><b>OpenAI API key errors</b></summary>

```
openai.AuthenticationError: Incorrect API key provided
```

**Solution:**
1. Verify your API key at [platform.openai.com](https://platform.openai.com/api-keys)
2. Ensure `OPENAI_API_KEY` is set correctly in `.env`
3. Check that you have sufficient credits/quota
</details>

<details>
<summary><b>ChromaDB permission errors</b></summary>

```
PermissionError: [Errno 13] Permission denied: './chroma_db'
```

**Solution:**
```bash
chmod -R 755 chroma_db/
```
</details>

<details>
<summary><b>Alembic migration errors</b></summary>

```
alembic.util.exc.CommandError: Can't locate revision identified by '...'
```

**Solution:**
```bash
# Reset migrations (WARNING: drops all tables)
alembic downgrade base
alembic upgrade head
```
</details>

---

## Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'feat: add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

### Commit Convention

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Purpose |
|:---|:---|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation changes |
| `refactor:` | Code refactoring |
| `test:` | Adding or updating tests |
| `chore:` | Maintenance tasks |

---

## License

This project is proprietary. All rights reserved.

---

<div align="center">

Built with FastAPI, LangChain, ChromaDB, and OpenAI

</div>
