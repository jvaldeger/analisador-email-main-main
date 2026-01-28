import requests
import json

# Emails de teste
test_emails = [
    {
        "text": "Prezados, gostaria de solicitar um orçamento para consultoria financeira. Precisamos analisar nosso fluxo de caixa para o próximo trimestre.",
        "expected": "Produtivo"
    },
    {
        "text": "Olá, bom dia! Só queria desejar um excelente final de semana a toda equipe. Abraços!",
        "expected": "Improdutivo"
    },
    {
        "text": "Segue em anexo a proposta comercial que discutimos na reunião. Por favor, analise e nos retorne com seu feedback até sexta-feira.",
        "expected": "Produtivo"
    }
]

# Testar API
for i, test in enumerate(test_emails, 1):
    print(f"\nTeste {i}:")
    print(f"Email: {test['text'][:50]}...")
    
    response = requests.post(
        "http://localhost:8000/api/classify",
        files={'email_text': (None, test['text'])}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"Categoria: {result['category']} (esperado: {test['expected']})")
        print(f"Confiança: {result['confidence']:.2%}")
        print(f"Resposta: {result['suggested_response'][:50]}...")
    else:
        print(f"Erro: {response.status_code} - {response.text}")