from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

app = FastAPI(
    title="Google Gemma4 Hackathon API",
    description="Cognitive Twin Backend API",
    version="1.0.0",
)

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# Request Model
# =========================
class UserInput(BaseModel):
    message: str


# =========================
# Routes
# =========================
@app.get("/")
def home():
    try:
        with open(
            "frontend/html/cognitive_twin_erd.html", "r", encoding="utf-8"
        ) as file:
            return HTMLResponse(content=file.read(), status_code=200)
    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/chat")
def chat(data: UserInput):
    user_message = data.message

    # Example AI logic
    response = f"Cognitive Twin Response: You said -> {user_message}"

    return {"user_input": user_message, "response": response}


# =========================
# Serve HTML Page
# =========================
@app.get("/ui", response_class=HTMLResponse)
def serve_ui():
    with open("cognitive_twin_erd.html", "r", encoding="utf-8") as file:
        return file.read()


# =========================
# Run Server
# =========================
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
