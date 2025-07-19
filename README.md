# 🧩 Think41 Workflow Definition API

This is a backend API built using **FastAPI** for managing workflows consisting of multiple steps with dependencies between them. The API allows users to create workflows, retrieve step execution orders using **topological sorting**, and detect cycles (invalid workflows).

---

## 🚀 Features

- Define workflows with multiple steps and dependencies
- Topologically sort steps to determine execution order
- Detect cycles in workflows (invalid dependencies)
- RESTful endpoints for creation and retrieval

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **FastAPI** (API framework)
- **Pydantic** (for validation)
- **Uvicorn** (ASGI server)

---

## 📦 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/think41-workflow-api.git
cd think41-workflow-api
````

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the FastAPI App

```bash
uvicorn main:app --reload
```

The app will be live at:
👉 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 📚 API Endpoints

### `POST /workflows/`

Create a new workflow with steps and their dependencies.

**Request Body:**

```json
{
  "name": "Workflow A",
  "steps": [
    {"name": "Step1", "prerequisites": []},
    {"name": "Step2", "prerequisites": ["Step1"]},
    {"name": "Step3", "prerequisites": ["Step1", "Step2"]}
  ]
}
```

---

### `GET /workflows/{workflow_id}`

Get sorted list of steps (topological order) for the workflow.

**Response:**

```json
{
  "workflow_id": "abc123",
  "execution_order": ["Step1", "Step2", "Step3"]
}
```

If there's a **cycle**, the API will respond with:

```json
{
  "error": "Cycle detected in the workflow."
}
```

---

## 🔁 Topological Sorting

The API uses **Kahn’s Algorithm** to:

* Validate workflow step dependencies
* Detect cycles (invalid configurations)
* Return correct step execution order

---

## 📂 Project Structure

```
.
├── main.py              # FastAPI app & routing
├── models.py            # Pydantic models
├── logic.py             # Topological sort and validation logic
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 👨‍💻 Author

Sahaj Yadav
[GitHub](https://github.com/sahajy)
