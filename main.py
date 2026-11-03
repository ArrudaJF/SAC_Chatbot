from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam
import json
import os
import auxiliares as aux

from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

# Mapeamento da função para o código poder chamá-la dinamicamente
funcoes_disponiveis = {
    "consultar_pedidos": aux.consultar_pedidos,
    "consultar_produtos": aux.consultar_produtos,
    "consultar_categorias": aux.consultar_categorias,
    "consultar_clientes": aux.consultar_clientes,
    "consultar_itens": aux.consultar_itens,
    "consultar_promocoes": aux.consultar_promocoes,
}

# Descrição da ferramenta em JSON Schema para o modelo entender como usá-la
with open('tools.json', 'r') as f:
    tools = json.load(f)

with open('system_file.txt', 'r') as f:
    system_file = f.read()

messages = [
    {"role": "system", "content": f'{system_file}'}
]

print("=== Sistema com Function Calling Iniciado ===")
print("Tente perguntar: 'Onde está meu pedido 123?'\n")

model_name = "nvidia/nemotron-3-ultra-550b-a55b:free"
# "meta-llama/llama-3.1-8b-instruct"

while True:
    user_input = input("Cliente: ")
    if user_input.lower() in ['sair', 'exit', 'quit']:
        break
        
    messages.append({"role": "user", "content": user_input})
    
    # Passo 1: Envia a pergunta e as ferramentas disponíveis (usando Llama 3.1 que suporta tools)
    response = client.chat.completions.create(
        model=model_name, 
        messages=messages, # type: ignore
        tools=tools,
        tool_choice="auto" # Deixa o modelo decidir se precisa chamar a função
    )
    
    response_message = response.choices[0].message
    
    # Verifica se o modelo decidiu chamar alguma função
    while(response_message.tool_calls):
        # Adiciona a intenção do modelo ao histórico
        messages.append(response_message) # type: ignore
        
        for tool_call in response_message.tool_calls:
            nome_funcao = tool_call.function.name # type: ignore
            # Converte os argumentos extraídos pelo modelo (JSON string) para um dicionário Python
            argumentos = json.loads(tool_call.function.arguments) # type: ignore
            
            print(f"[Sistema executando função local: {nome_funcao}({argumentos})]...")
            
            # Executa a função local real
            funcao_real = funcoes_disponiveis[nome_funcao]
            resultado_funcao = funcao_real(**argumentos)
            
            # Passo 2: Devolve o resultado da função para o modelo
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": nome_funcao,
                "content": str(resultado_funcao)
            })
            
        # Passo 3: Pede ao modelo para gerar a resposta final em linguagem natural
        second_response = client.chat.completions.create(
            model=model_name, 
            messages=messages # type: ignore
        )
        response_message = second_response.choices[0].message
        
    # O modelo respondeu diretamente, sem usar ferramentas
    bot_reply = response_message.content
    print(f"Agente: {bot_reply}\n")
    messages.append({"role": "assistant", "content": bot_reply}) # type: ignore