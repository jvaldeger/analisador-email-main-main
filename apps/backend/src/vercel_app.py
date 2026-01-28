from fastapi import FastAPI
import sys

from fastapi import File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

from .classifiers.nlp_classifier import EmailClassifier
from .utils.text_processor import extract_text_from_file
from .models.schemas import EmailResponse


app = FastAPI(
    title="Email Classifier API",
    description="API para classificar emails como Produtivo ou Improdutivo e gerar respostas automáticas",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["analisador-email-frontend-git-main-projects.vercel.app","*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/classify", response_model=EmailResponse)
async def classify_email(
    email_text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """
    CLASSIFICAÇÃO DOS EMAILS IMPRODUTIVOS OU PRODUTIVOS
    """
    try:
        #
        if email_text:
            text = email_text.strip()
        elif file:
            text = await extract_text_from_file(file)
        else:
            raise HTTPException(
                status_code=400, 
                detail="No input provided. Please provide either email_text or a file."
            )
        
        if not text or len(text) < 10:

            print("Text is too short or empty.")
            raise HTTPException(
                status_code=400,
                detail="Text is too short or empty. Minimum 10 characters required."
            )
        
        # CLASSIFICAÇÃO EMAIL
        category, confidence = EmailClassifier().classify(text)
        preview = text[:100] + "..." if len(text) > 100 else text
        
        print(f"Classified as {category} with confidence {confidence:.2f}")
        return EmailResponse(
            category=category,
            confidence=confidence,
            suggested_response="suggested_response",
            original_text_preview=preview
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "python": sys.version,
        "message": "API rodando"
    }

@app.get("/")
async def root():
    return {
        "message": "Email Classifier API",
        "version": "1.0.0"
    }

print("✅ App FastAPI criado com sucesso!")