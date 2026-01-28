import pdfplumber
import io
from typing import Union
from fastapi import UploadFile

async def extract_text_from_file(file: UploadFile) -> str:
    """
    Extract text from uploaded file (PDF or TXT)
    Using pdfplumber for PDF extraction
    """
    if file.filename.endswith('.pdf'):
        # Extract text from PDF using pdfplumber
        try:
            text = ""
            content = await file.read()
            # Use BytesIO to handle PDF bytes
            with pdfplumber.open(io.BytesIO(content)) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text.strip() if text else "Não foi possível extrair texto do PDF"
        except Exception as e:
            raise ValueError(f"Erro ao extrair texto do PDF: {str(e)}")
    
    elif file.filename.endswith('.txt'):
        # Decode text file
        content = await file.read()
        return content.decode('utf-8')
    
    else:
        raise ValueError("Formato de arquivo não suportado. Use PDF ou TXT.")