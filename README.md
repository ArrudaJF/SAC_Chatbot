# SAC_Chatbot
Uma LLM de atendimento ao cliente de uma loja fictícia 'Empório da Música'

# Execução do código:
Certifique-se de ter o Python instalado na sua máquina (versão 3.8 ou superior). 

Crie um Virtual Environment com:

```bash
py -m venv .venv
```

Ative o venv:

```bash
./.venv/Scripts/activate
```

Você precisará instalar as bibliotecas do arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

## Crie uma conta no OpenRouter:

1. Crie uma conta no OpenRouter e gere uma chave de API.

2. Na raiz do projeto, crie um arquivo chamado .env.

3. Adicione a sua chave de API no arquivo .env com a seguinte estrutura:
```
Snippet de código
API_KEY=sk-or-v1-sua-chave-api-aqui
```

## Como Executar:
```bash
streamlit run app.py
```

Um site http://localhost:8501 irá abrir e o chat será inicializado



# Decisões Técnicas:

Três grandes decisões devem ser destacadas que são, a escolha de modelo, a escolha das libs OpenRouter e StreamLit.

É inviável baixar o modelo para rodar local, então a opção mais acertada seria usar uma API para poder usar algum modelo mais robusto e bem treinado. 
Como já trabalhei com o OpenRouter no meu estágio, trouxe essa implementação para o case, podemos usar modelos grátis e podemos criar uma chave de API grátis
  e dá um retorno legal. O StreamLit é outra biblioteca que já havia utilizado anteriormente e ela será usada para a interface, claro que a interface 
  não era o foco da implementação, mas achei uma boa relação entre a facilidade de implementar com o resultado.

Quanto a escolha de modelo, testei dois modelos "nvidia/nemotron-3-ultra-550b-a55b:free" e "meta-llama/llama-3.1-8b-instruct", o modelo da nvidia é um dos melhores e mais robustos que achei dentre os gratuitos no OpenRouter e é um modelo focado em raciocínio, agentes autônomos e fluxos de trabalho complexos, achei uma boa opção pro contexto aqui, é o que recomendo usar. Enquanto o llama3.1 é um classico, leve e suficiente pro trabalho.

No código, a LLM vai ter a liberdade de executar algumas funções para consultar dados externos, assim o agente tem pouco espaço para alucinações, pois estará lendo documentos com as informações explícitas.

Algumas coisas podem ser melhores, poderia usar um Vector Database para lidar melhor com os dados e obviamente, a questão de segurança. O agente ainda pode ser flexibilizado para mudar de função ou enviar dados sensíveis se feita uma boa engenharia de prompt por parte do usuário. Ele é um pouco lento, mais do que gostaria, mas acho que é bem consertável. Além disso, às vezes ele fala coisas que não deixo claro que podem ser feitas, como reservar instrumentos, mas se fosse aplicado na vida real, ele seria fine-tunado e melhor trabalhado então tenho uma boa ideia de coo consertar essas questões.

Usei o gemini Pro para consertar algumas coisas que não sabia como, especialmente com o streamlit, mas me limitei a consertar bugs e encontrar erros ao invés de, de fato, pedir para a IA gerar o código pronto, ainda prefiro codar por mim mesmo. De modo geral foi divertido implementar e deu mais vontade de saber mais sobre a empresa. 