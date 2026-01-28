from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import os
import sys


sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from classifiers.nlp_classifier import EmailClassifier
from classifiers.response_generator import ResponseGenerator
from utils.text_processor import extract_text_from_file
from models.schemas import EmailResponse

app = FastAPI(
    title="Email Classifier API",
    description="API para classificar emails como Produtivo ou Improdutivo e gerar respostas automáticas",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


classifier = None
response_gen = None

def get_classifier():
    global classifier
    if classifier is None:
        classifier = EmailClassifier()
    return classifier

def get_response_generator():
    global response_gen
    if response_gen is None:
        response_gen = ResponseGenerator()
    return response_gen

@app.post("/api/classify", response_model=EmailResponse)
async def classify_email(
    email_text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None)
):
    """
    CLASSIFICAÇÃO DOS EMAILS
    """
   
    try:
        
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
        
        # Get classificação
        classifier = get_classifier()
        response_gen = get_response_generator()
        
        # Classificação email
        category, confidence = classifier.classify(text)
    
        suggested_response = response_gen.generate_response(text, category)
        
        preview = text[:100] + "..." if len(text) > 100 else text
        
        print(f"Classified as {category} with confidence {confidence:.2f}")
        return EmailResponse(
            category=category,
            confidence=confidence,
            suggested_response=suggested_response,
            original_text_preview=preview
        )
        
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/")
async def root():
    return {
        "message": "Email Classifier API",
        "version": "1.0.0",
        "endpoints": {
            "POST /api/classify": "Classify email and generate response",
            "GET /health": "Health check",
            "GET /": "This info page"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "Email Classifier API",
        "timestamp": __import__("datetime").datetime.now().isoformat()
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))