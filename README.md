# SAC_Chatbot
Uma LLM de atendimento ao cliente de uma loja fictícia 'Empório da Música'

# Execução do código:
Certifique-se de ter o Python instalado na sua máquina (versão 3.8 ou superior). 
Você precisará instalar as bibliotecas do arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

# Crie uma conta no OpenRouter:

1. Crie uma conta no OpenRouter e gere uma chave de API.

2. Na raiz do projeto, crie um arquivo chamado .env.

3. Adicione a sua chave de API no arquivo .env com a seguinte estrutura:
```
Snippet de código
API_KEY=sk-or-v1-sua-chave-api-aqui
```

# Como Executar:
```bash
streamlit run app.py
```

Um site http://localhost:8501 irá abrir e o chat será inicializado