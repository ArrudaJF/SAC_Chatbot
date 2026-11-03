from openai import OpenAI
import json
import os
import auxiliares as aux
import streamlit as st
from dotenv import load_dotenv

st.title("Agente de SAC - Empório da Música")

load_dotenv()
api_key = os.getenv("API_KEY")

client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

funcoes_disponiveis = {
    "consultar_politica": aux.consultar_politica,
    "consultar_pedidos": aux.consultar_pedidos,
    "consultar_produtos": aux.consultar_produtos,
    "consultar_categorias": aux.consultar_categorias,
    "consultar_clientes": aux.consultar_clientes,
    "consultar_itens": aux.consultar_itens,
    "consultar_promocoes": aux.consultar_promocoes,
}

with open('tools.json', 'r') as f:
    tools = json.load(f)

with open('system_file.txt', 'r') as f:
    system_file = f.read()

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "nvidia/nemotron-3-ultra-550b-a55b:free"

if "messages" not in st.session_state:
    st.session_state.messages = [ {"role": "system", "content": system_file} ]

# CORREÇÃO 4: Renderiza APENAS mensagens de usuário e assistente que possuem texto
for message in st.session_state.messages:
    if message["role"] in ["user", "assistant"] and message.get("content"):
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Como posso ajudar?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)

    # CORREÇÃO 2: Passa a lista completa de dicionários em vez de filtrar chaves importantes
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=st.session_state.messages,
        tools=tools,
        tool_choice="auto"
    ) 
    response_message = response.choices[0].message

    # Loop para caso ele queira chamar múltiplas ferramentas em sequência
    while response_message.tool_calls:
        
        # CORREÇÃO 1: Adiciona a requisição da ferramenta feita pelo assistente ao histórico
        # O .model_dump() converte o objeto da OpenAI num dicionário seguro para o Streamlit
        st.session_state.messages.append(response_message.model_dump(exclude_none=True))
        
        for tool_call in response_message.tool_calls:
            nome_funcao = tool_call.function.name
            argumentos = json.loads(tool_call.function.arguments) 
            
            print(f"[Sistema executando função local: {nome_funcao}({argumentos})]...")
            
            # Executa a função local real
            funcao_real = funcoes_disponiveis[nome_funcao]
            resultado_funcao = funcao_real(**argumentos)
            
            # Devolve o resultado da função para o modelo
            st.session_state.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": nome_funcao,
                "content": str(resultado_funcao)
            })
            
        # Pede ao modelo para processar os dados recebidos e gerar texto (ou chamar mais ferramentas)
        second_response = client.chat.completions.create(
            model=st.session_state["openai_model"], 
            messages=st.session_state.messages, 
            tools=tools,
            tool_choice="auto"
        )
        response_message = second_response.choices[0].message
        
    # O modelo respondeu diretamente com texto (após usar ou não ferramentas)
    bot_reply = response_message.content

    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    # CORREÇÃO 3: Salva o texto da resposta (`bot_reply`) no histórico, não o retorno do `st.write`
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})