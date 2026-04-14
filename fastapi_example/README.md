# FastAPI Frontend ↔ Backend Example

This example demonstrates how to connect a simple frontend to a FastAPI backend.

## Backend

Run the FastAPI server:

```bash
pip install -r requirements.txt
python backend/main.py
```

The server exposes `GET /api/message` which returns a JSON message.

## Frontend

Open `frontend/index.html` in a browser. It uses the Fetch API to request the message from the backend and displays the response on the page.
