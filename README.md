# Agentic AI-Powered API Error Diagnosis System 🤖🔍

Welcome to the **Antigravity Agentic Debugger**. This system autonomously detects, diagnoses, and resolves (or recommends fixes for) API errors using a multi-agent LangChain/LangGraph architecture.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- OpenAI API Key (Set as `OPENAI_API_KEY` in environment variables or `.env` file)

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Gokul26092004/Antigravity.git
cd Antigravity
pip install -r requirements.txt
```

### 2. Run the Web UI
Start the FastAPI server:
```bash
python -m uvicorn server:app --host 0.0.0.0 --port 8000
```
Then open your browser to: **`http://localhost:8000`**

---

## 🛠️ How to Use the Tutorial Case

To see the system in action, follow these steps:

1.  **Copy this Example Log:**
    ```text
    ERROR 2023-10-27 10:00:01 com.example.db.ConnectionManager - 
    Failed to connect to jdbc:postgresql://db-prod:5432/users
    org.postgresql.util.PSQLException: Connection to localhost:5432 refused.
    ```
2.  **Paste** it into the "ERROR LOG INPUT" section on the website.
3.  **Click "INITIATE DIAGNOSIS"**.
4.  **Observe the Neural Feed:**
    *   **Analyzer**: Parses the raw stack trace.
    *   **Investigator**: Searches logs and deployment history.
    *   **Diagnoser**: Deduces that a security group or bad deployment is the cause.
    *   **Fix Generator**: Proposes a Terraform fix or a Git rollback.
    *   **Validator**: Verifies the fix in a sandbox environment.
    *   **Risk Assessor**: Approves the action (if it's a low-risk rollback).

---

## 🧠 Meet the Squad (Agent Roles)

| Role | Responsibility |
| :--- | :--- |
| **Supervisor** | Orchestrates the state graph and routes tasks. |
| **Error Analyzer** | Structurally breaks down unhandled exceptions. |
| **Log Investigator** | Queries ELK/Datadog and Git history for context. |
| **Root Cause Reasoner** | Synthesizes all data to find the *why*. |
| **Fix Generator** | Proposes code patches or infrastructure changes. |
| **Risk Assessor** | Safety gate that blocks high-risk autonomous actions. |

---

## 🛡️ Safety Features
*   **Human-in-the-Loop**: High-risk changes (like direct code edits) are proposed as Draft PRs.
*   **Read-Only Investigation**: Investigation agents do not have write access to your production DB.
*   **Risk Grading**: Actions are graded (LOW/HIGH risk) before execution.

---

Built with 💜 using [LangChain](https://github.com/langchain-ai/langchain) and [LangGraph](https://github.com/langchain-ai/langgraph).
