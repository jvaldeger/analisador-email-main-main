import nltk
import os
from nltk.corpus import stopwords
from nltk.stem import RSLPStemmer
from nltk.util import ngrams
import re
from typing import Tuple, List, Set

# ========== CONFIGURAÇÃO NLTK PARA VERCEL ==========
# Configurar NLTK para usar diretório temporário no Vercel
nltk_data_path = '/tmp/nltk_data'

# Adiciona o caminho do temp ao path do NLTK
nltk.data.path.append(nltk_data_path)

# Tenta criar o diretório (pode falhar em alguns ambientes, mas tenta mesmo assim)
try:
    os.makedirs(nltk_data_path, exist_ok=True)
except:
    pass

# Download NLTK
nltk_resources = ['punkt', 'stopwords', 'rslp']
for resource in nltk_resources:
    try:
        if resource == 'punkt':
            nltk.data.find(f'tokenizers/{resource}')
        else:
            nltk.data.find(f'corpora/{resource}')
        print(f"✅ Recurso NLTK '{resource}' já disponível em {nltk_data_path}")
    except LookupError:
        print(f"⚠️  Recurso NLTK '{resource}' não encontrado, tentando baixar...")
        try:
            # Tenta baixar para o diretório temp
            nltk.download(resource, download_dir=nltk_data_path, quiet=True)
            print(f"✅ Recurso NLTK '{resource}' baixado com sucesso")
        except Exception as e:
            print(f"❌ Não foi possível baixar o recurso '{resource}': {e}")
            print("📦 Continuando sem este recurso do NLTK...")

class EmailClassifier:
    def __init__(self):
        
        self.classifier = None
        self.stemmer = RSLPStemmer()
        try:
            self.stop_words = set(stopwords.words('portuguese'))
        except:
            print("⚠️  Não foi possível carregar stopwords do NLTK, usando lista manual")
            # Lista básica de stopwords em português como fallback
            self.stop_words = {
                'de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para',
                'é', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por',
                'mais', 'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele',
                'das', 'tem', 'à', 'seu', 'sua', 'ou', 'ser', 'quando',
                'muito', 'há', 'nos', 'já', 'está', 'eu', 'também', 'só'
            }
        
        
        self.improdutivo_unigrams = set()
        self.improdutivo_bigrams = set()
        self.improdutivo_trigrams = set()
        self.produtivo_unigrams = set()
        self.produtivo_bigrams = set()
        self.produtivo_trigrams = set()
        self._initialize_keywords()
        self.weights = {
            'unigram': 1.0,
            'bigram': 2.0,
            'trigram': 3.0
        }
        
        print("✅ Classificador de emails inicializado com sucesso")
    
    def _initialize_keywords(self):

        improdutivo_keyword_list = [
            'saudação', 'cumprimento', 'veneração', 'reverência', 'homenagem',
            'cortesia', 'gentileza', 'fineza', 'atenção', 'consideração',
            'olá', 'oi', 'alô', 'bomdia', 'boatarde',
            'boanoite', 'saudações', 'saúdo', 'saudável', 'cumprimentar',
            'adeus', 'tchau', 'atélogo', 'atébreve', 'atémais',
            'agradecimento', 'gratidão', 'reconhecimento', 'obrigado', 'grato',
            'parabéns', 'felicitações', 'congratulações', 'beneplácito', 'exultação',
            'elogio', 'louvor', 'enaltecimento', 'encômio', 'apologia'
        ]
        
        produtivo_keyword_list = [
            'proposta', 'contrato', 'aditivo', 'escritura', 'procuração',
            'pagamento', 'fatura', 'orçamento', 'financiamento', 'empréstimo',
            'venda', 'compra', 'negócio', 'transação', 'aquisição',
            'projeto', 'entrega', 'serviço', 'produto', 'metodologia',
            'cronograma', 'prazo', 'etapa', 'fase', 'marco',
            'cláusula', 'penalidade', 'multa', 'indenização', 'arbitragem',
            'admissão', 'demissão', 'rescisão', 'folha', 'ponto',
            'software', 'hardware', 'aplicativo', 'plataforma', 'nuvem',
            'estoque', 'inventário', 'armazenamento', 'distribuição', 'logística'
        ]
        
      
        self.improdutivo_unigrams = set(improdutivo_keyword_list)
        self.produtivo_unigrams = set(produtivo_keyword_list)      
        self._generate_ngrams_from_keywords(improdutivo_keyword_list, produtivo_keyword_list)
        self._add_manual_ngrams()
    
    def _generate_ngrams_from_keywords(self, improdutivo_list, produtivo_list):
        improdutivo_bigrams = self._create_ngrams_from_list(improdutivo_list, 2)
        improdutivo_trigrams = self._create_ngrams_from_list(improdutivo_list, 3)
        

        produtivo_bigrams = self._create_ngrams_from_list(produtivo_list, 2)
        produtivo_trigrams = self._create_ngrams_from_list(produtivo_list, 3)
        
        self.improdutivo_bigrams.update(improdutivo_bigrams)
        self.improdutivo_trigrams.update(improdutivo_trigrams)
        self.produtivo_bigrams.update(produtivo_bigrams)
        self.produtivo_trigrams.update(produtivo_trigrams)
    
    def _create_ngrams_from_list(self, word_list: List[str], n: int) -> Set[str]:
        ngrams_set = set()
        for i in range(len(word_list) - n + 1):
            ngram = ' '.join(word_list[i:i+n])
            ngrams_set.add(ngram)
        return ngrams_set
    
    def _add_manual_ngrams(self):
        manual_improdutivo_bigrams = {
            'bom dia', 'boa tarde', 'boa noite', 'até logo', 'até breve',
            'muito obrigado', 'muito grato', 'parabéns pelo', 'feliz aniversário',
            'com licença', 'por favor', 'me desculpe', 'sinto muito',
            'tudo bem', 'como vai', 'estou bem', 'tenha um', 'ótimo dia'
        }
        
        manual_improdutivo_trigrams = {
            'tenha um bom', 'um bom dia', 'boa tarde a', 'tarde a todos',
            'muito obrigado pela', 'obrigado pela atenção', 'feliz aniversário meu',
            'com licença pode', 'por favor pode', 'me desculpe pelo'
        }

        manual_produtivo_bigrams = {
            'proposta comercial', 'contrato de', 'pagamento da', 'fatura número',
            'orçamento aprovado', 'reunião de', 'relatório de', 'projeto de',
            'prazo de entrega', 'entrega do', 'serviço prestado', 'produto final',
            'cronograma de', 'metodologia ágil', 'cláusula contratual', 'multa por',
            'indenização por', 'admissão de', 'demissão sem', 'software de',
            'hardware necessário', 'estoque de', 'inventário físico', 'logística de'
        }
        
        manual_produtivo_trigrams = {
            'contrato de prestação', 'pagamento da fatura', 'fatura número de',
            'orçamento aprovado pelo', 'reunião de trabalho', 'relatório de atividades',
            'projeto de implementação', 'prazo de entrega do', 'entrega do produto',
            'serviço prestado pela', 'cronograma de atividades', 'metodologia ágil scrum',
            'cláusula contratual de', 'multa por atraso', 'indenização por danos',
            'admissão de funcionário', 'demissão sem justa', 'software de gestão',
            'hardware necessário para', 'estoque de produtos', 'inventário físico de'
        }
        
      
        self.improdutivo_bigrams.update(manual_improdutivo_bigrams)
        self.improdutivo_trigrams.update(manual_improdutivo_trigrams)
        self.produtivo_bigrams.update(manual_produtivo_bigrams)
        self.produtivo_trigrams.update(manual_produtivo_trigrams)
    
    def extract_ngrams(self, tokens: List[str]) -> Tuple[List[str], List[str], List[str]]:
        unigrams = tokens
        
        # Bigramas
        bigrams = []
        if len(tokens) >= 2:
            bigrams = [' '.join(bigram) for bigram in ngrams(tokens, 2)]
        
        # Trigramas
        trigrams = []
        if len(tokens) >= 3:
            trigrams = [' '.join(trigram) for trigram in ngrams(tokens, 3)]
        
        return unigrams, bigrams, trigrams
    
    def tokenize_with_fallback(self, text: str) -> List[str]:
        try:
            words = nltk.word_tokenize(text, language='portuguese')
        except Exception as e:
            print(f"⚠️  NLTK tokenize falhou, usando fallback simples: {e}")
            # Fallback simples: dividir por espaços e caracteres não alfanuméricos
            words = re.findall(r'\b\w+\b', text.lower())
        
        return words
    
    def preprocess_text(self, text: str) -> Tuple[List[str], List[str], List[str]]:
        text = text.lower()
        text = re.sub(r'[^\w\sáàâãéèêíïóôõöúçñ]', ' ', text, flags=re.UNICODE)
        text = re.sub(r'\d+', '', text)
        words = self.tokenize_with_fallback(text)
        words = [word for word in words if word not in self.stop_words and len(word) > 2]
        try:
            words = [self.stemmer.stem(word) for word in words]
        except Exception as e:
            print(f"⚠️  Stemming falhou: {e}")

        unigrams, bigrams, trigrams = self.extract_ngrams(words)
        
        return unigrams, bigrams, trigrams
    
    def calculate_ngram_scores(self, text_unigrams: List[str], 
                               text_bigrams: List[str], 
                               text_trigrams: List[str]) -> Tuple[float, float]:
        produtivo_score = 0.0
        improdutivo_score = 0.0
        
        
        for unigram in text_unigrams:
            if unigram in self.produtivo_unigrams:
                produtivo_score += self.weights['unigram']
            if unigram in self.improdutivo_unigrams:
                improdutivo_score += self.weights['unigram']
        
        
        for bigram in text_bigrams:
            if bigram in self.produtivo_bigrams:
                produtivo_score += self.weights['bigram']
            if bigram in self.improdutivo_bigrams:
                improdutivo_score += self.weights['bigram']
        
     
        for trigram in text_trigrams:
            if trigram in self.produtivo_trigrams:
                produtivo_score += self.weights['trigram']
            if trigram in self.improdutivo_trigrams:
                improdutivo_score += self.weights['trigram']
        
        return produtivo_score, improdutivo_score
    
    def classify_with_rules(self, text: str) -> Tuple[str, float]:
        unigrams, bigrams, trigrams = self.preprocess_text(text)
        
        
        produtivo_score, improdutivo_score = self.calculate_ngram_scores(
            unigrams, bigrams, trigrams
        )
        
       
        total_score = produtivo_score + improdutivo_score
        
        if total_score == 0:
            return "Produtivo", 0.5  
        
        # Calcular confiança
        produtivo_ratio = produtivo_score / total_score
        improdutivo_ratio = improdutivo_score / total_score
        
        if produtivo_ratio > improdutivo_ratio:
            confidence = min(0.95, 0.5 + (produtivo_ratio * 0.5))
            return "Produtivo", confidence
        elif improdutivo_ratio > produtivo_ratio:
            confidence = min(0.95, 0.5 + (improdutivo_ratio * 0.5))
            return "Improdutivo", confidence
        else:
            produtivo_count = len([ngram for ngram in unigrams + bigrams + trigrams 
                                 if ngram in self.produtivo_unigrams or 
                                 ngram in self.produtivo_bigrams or 
                                 ngram in self.produtivo_trigrams])
            improdutivo_count = len([ngram for ngram in unigrams + bigrams + trigrams 
                                   if ngram in self.improdutivo_unigrams or 
                                   ngram in self.improdutivo_bigrams or 
                                   ngram in self.improdutivo_trigrams])
            
            if produtivo_count > improdutivo_count:
                return "Produtivo", 0.6
            elif improdutivo_count > produtivo_count:
                return "Improdutivo", 0.6
            else:
                return "Produtivo", 0.5  # Default Produtivo
    
    def find_key_ngrams(self, text: str, category: str = "both") -> dict:
        unigrams, bigrams, trigrams = self.preprocess_text(text)
        
        result = {
            "produtivo": {"unigrams": [], "bigrams": [], "trigrams": []},
            "improdutivo": {"unigrams": [], "bigrams": [], "trigrams": []}
        }
        
        if category in ["both", "produtivo"]:
            result["produtivo"]["unigrams"] = [u for u in unigrams if u in self.produtivo_unigrams]
            result["produtivo"]["bigrams"] = [b for b in bigrams if b in self.produtivo_bigrams]
            result["produtivo"]["trigrams"] = [t for t in trigrams if t in self.produtivo_trigrams]
        
        if category in ["both", "improdutivo"]:
            result["improdutivo"]["unigrams"] = [u for u in unigrams if u in self.improdutivo_unigrams]
            result["improdutivo"]["bigrams"] = [b for b in bigrams if b in self.improdutivo_bigrams]
            result["improdutivo"]["trigrams"] = [t for t in trigrams if t in self.improdutivo_trigrams]
        
        return result
    
    def classify(self, text: str) -> Tuple[str, float]:
        if not text or len(text.strip()) < 10:
            return "Improdutivo", 0.5
        
        try:
            return self.classify_with_rules(text)
                
        except Exception as e:
            print(f"Classification error: {e}")
            text_lower = text.lower()
            if any(word in text_lower for word in ['reunião', 'contrato', 'projeto', 'relatório', 'prazo', 'entrega']):
                return "Produtivo", 0.6
            elif any(word in text_lower for word in ['olá', 'oi', 'bom dia', 'obrigado', 'parabéns']):
                return "Improdutivo", 0.6
            else:
                return "Produtivo", 0.5


# Exemplo de uso
if __name__ == "__main__":
    classifier = EmailClassifier()
    
    # Exemplo de emails
    emails = [
        "Olá, bom dia! Espero que esteja tudo bem com você. Um abraço!",
        "Prezados, segue em anexo a proposta comercial para revisão. Favor analisar até sexta-feira.",
        "Caros colegas, convido todos para a reunião de alinhamento do projeto às 10h.",
        "Oi! Tudo bem? Vamos marcar um café essa semana?",
        "Segue fatura número 12345 com vencimento para 30/11. Favor providenciar pagamento."
    ]
    
    for email in emails:
        category, confidence = classifier.classify(email)
        print(f"Email: {email[:50]}...")
        print(f"Classificação: {category} (Confiança: {confidence:.2f})")
        
        # Mostrar n-grams encontrados
        key_ngrams = classifier.find_key_ngrams(email, "both")
        print("N-grams produtivos encontrados:", key_ngrams["produtivo"])
        print("N-grams improdutivos encontrados:", key_ngrams["improdutivo"])
        print("-" * 50)