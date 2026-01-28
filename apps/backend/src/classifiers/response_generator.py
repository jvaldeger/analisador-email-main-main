import os
from typing import Literal
import random

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class ResponseGenerator:
    def __init__(self):
        self.use_openai = False
        
        if OPENAI_AVAILABLE:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                openai.api_key = api_key
                self.use_openai = True
            else:
                print("Warning: OPENAI_API_KEY not found. Using local response generation.")
        else:
            print("Warning: OpenAI not installed. Using local response generation.")
    
    def generate_local_response(self, email_text: str, category: Literal["Produtivo", "Improdutivo"]) -> str:
        if category == "Produtivo":
            templates = [
                "Agradecemos seu contato. Sua solicitação foi registrada sob o protocolo #{} e será analisada por nossa equipe em até 48 horas úteis. Em caso de urgência, entre em contato através do telefone (11) 9999-9999.",
                "Recebemos sua mensagem e agradecemos pelo contato. Nossa equipe especializada está analisando sua solicitação e retornaremos em breve com uma resposta completa. Para questões urgentes, nosso horário de atendimento é de segunda a sexta, das 9h às 18h.",
                "Confirmamos o recebimento do seu email. Sua demanda está sendo processada e você receberá um retorno em até 3 dias úteis. Caso necessite de informações adicionais, não hesite em nos contactar."
            ]
        else:
            templates = [
                "Agradecemos sua mensagem e os sentimentos compartilhados. Desejamos um ótimo dia e estamos à disposição para qualquer necessidade futura.",
                "Obrigado pelo contato e pelas palavras. Ficamos contentes com sua mensagem e desejamos sucesso em suas atividades. Atenciosamente,",
                "Agradecemos seu email. É sempre um prazer receber seu contato. Desejamos uma excelente semana e permanecemos à disposição."
            ]
        
        protocol = random.randint(10000, 99999)
        response = random.choice(templates)
        return response.format(protocol) if "{}" in response else response
    
    def generate_openai_response(self, email_text: str, category: Literal["Produtivo", "Improdutivo"]) -> str:
        if category == "Produtivo":
            prompt = f"""
            Você é um assistente de uma empresa financeira. Gere uma resposta profissional e útil para o seguinte email.
            A resposta deve: 1) Agradecer pelo contato, 2) Reconhecer a solicitação, 3) Informar que será processada,
            4) Fornecer um prazo estimado, 5) Oferecer ajuda adicional se necessário.
            
            Email recebido: {email_text[:500]}
            
            Resposta (em português brasileiro, máximo 150 palavras):
            """
        else:
            prompt = f"""
            Você é um assistente de uma empresa financeira. Gere uma resposta educada e genérica para um email de cumprimentos ou agradecimento.
            A resposta deve ser: 1) Agradecida, 2) Breve, 3) Cordial, 4) Encerrar de forma positiva.
            
            Email recebido: {email_text[:500]}
            
            Resposta (em português brasileiro, máximo 100 palavras):
            """
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um assistente profissional de uma empresa financeira."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI error: {e}")
            return self.generate_local_response(email_text, category)
    
    def generate_response(self, email_text: str, category: Literal["Produtivo", "Improdutivo"]) -> str:
        if self.use_openai:
            return self.generate_openai_response(email_text, category)
        else:
            return self.generate_local_response(email_text, category)