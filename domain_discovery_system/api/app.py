from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import uvicorn

from domain_discovery_system.api.routes.static_question import (
    router as static_question_router,
)

# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="Google Gemma4 Hackathon API",
    description="Cognitive Twin Backend API",
    version="1.0.0",
)

# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================================
# REQUEST MODEL
# =========================================================


class UserInput(BaseModel):

    message: str


# =========================================================
# HOME ROUTE
# =========================================================


@app.get("/")
def home():

    try:

        with open(
            "frontend/html/cognitive_twin_erd.html",
            "r",
            encoding="utf-8",
        ) as file:

            return HTMLResponse(
                content=file.read(),
                status_code=200,
            )

    except Exception as e:

        return {
            "status": "error",
            "message": str(e),
        }


# =========================================================
# HEALTH CHECK
# =========================================================


@app.get("/health")
def health_check():

    return {"status": "healthy"}


# =========================================================
# CHAT ROUTE
# =========================================================

# =========================================================
# CHAT ROUTE
# =========================================================

from domain_discovery_system.ai.gemma_service import (
    generate_response,
)


@app.post("/chat")
def chat(data: UserInput):

    try:

        user_message = data.message

        print("\n===================================")
        print("USER MESSAGE")
        print("===================================\n")

        print(user_message)

        # =========================================
        # GEMMA RESPONSE
        # =========================================

        ai_response = generate_response(user_message)

        print("\n===================================")
        print("AI RESPONSE")
        print("===================================\n")

        print(ai_response)

        # =========================================
        # RETURN RESPONSE
        # =========================================

        return {
            "status": "success",
            "user_input": user_message,
            "ai_response": ai_response,
        }

    except Exception as e:

        print("\n===================================")
        print("CHAT ROUTE ERROR")
        print("===================================\n")

        print(str(e))

        return {
            "status": "error",
            "message": str(e),
        }


# =========================================================
# SERVE UI
# =========================================================


@app.get("/ui", response_class=HTMLResponse)
def serve_ui():

    try:

        with open(
            "frontend/html/cognitive_twin_erd.html",
            "r",
            encoding="utf-8",
        ) as file:

            return file.read()

    except Exception as e:

        return HTMLResponse(
            content=f"<h1>{str(e)}</h1>",
            status_code=500,
        )


# =========================================================
# REGISTER ROUTES
# =========================================================

app.include_router(static_question_router)

# =========================================================
# RUN SERVER
# =========================================================

if __name__ == "__main__":

    uvicorn.run(
        "domain_discovery_system.api.app:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
