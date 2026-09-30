from pathlib import Path                      
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.models import (
    QARequest,
    ExplainRequest,
    QuizRequest,
    SummaryRequest,
    LearningPathRequest,
)

from app.services.qna import answer_question
from app.services.explanation_module import explain_topic
from app.services.quiz_module import generate_quiz
from app.services.summary_module import summarize_text
from app.services.learning_path import get_learning_recommendations


app = FastAPI(
    title="EduGenie",
    description="Google Gemini Powered Learning Assistant",
    version="1.0.0",
)


# Static files
BASE_DIR = Path(__file__).resolve().parent

app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static"
)



# HTML templates
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)
# --------------------------------------------------
# HOME PAGE
# --------------------------------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie"
    }


# --------------------------------------------------
# QUESTION ANSWERING
# --------------------------------------------------

@app.post("/qa")
async def qa(payload: QARequest):

    try:
        answer = answer_question(payload.question)

        return {
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# EXPLANATION
# --------------------------------------------------

@app.post("/explain")
async def explain(payload: ExplainRequest):

    try:
        answer = explain_topic(
            payload.topic,
            payload.level
        )

        return {
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# QUIZ GENERATION
# --------------------------------------------------

@app.post("/quiz")
async def quiz(payload: QuizRequest):

    try:
        quiz = generate_quiz(
            payload.text,
            payload.level,
            payload.count
        )

        return {
            "quiz": quiz
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# SUMMARIZATION
# --------------------------------------------------

@app.post("/summarize")
async def summarize(payload: SummaryRequest):

    try:
        summary = summarize_text(
            payload.text,
            payload.max_words
        )

        return {
            "summary": summary
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# --------------------------------------------------
# LEARNING PATH
# --------------------------------------------------

@app.post("/learn/recommendations")
async def learning_path(payload: LearningPathRequest):

    try:
        recommendations = get_learning_recommendations(
            payload.topic,
            payload.level,
            payload.weeks
        )

        return {
            "recommendations": recommendations
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )