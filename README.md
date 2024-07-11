### Travel Agent API

Este projeto implementa uma API de agente de viagens que utiliza inteligência artificial para fornecer informações detalhadas sobre viagens. Ele utiliza a linguagem natural para compreender e responder a consultas dos usuários, incluindo eventos, preços de passagens, pontos turísticos, restaurantes recomendados e dicas extras.

Este projeto envolve a construção de um contêiner Docker que foi transformado em uma API disponível na AWS. A integração inclui modelos de Linguagem de Longa Memória (LLM), como o GPT-3.5 Turbo, que foram aprimorados com dados do Wikipedia, DuckDuckGo e outros recursos específicos da web. Essa implementação não só demonstra um caso de uso para agentes de viagens, mas também destaca a flexibilidade do modelo, permitindo adaptações para uma ampla gama de aplicações através da configuração de padrões e parâmetros adequados.

#### Funções Principais:

- **ChatOpenAI**: Integração com GPT-3.5 Turbo para conversação em linguagem natural.
- **Agent Executor**: Orquestração de agentes de pesquisa e geração de respostas utilizando ferramentas de busca e Wikipedia.
- **RAG Agent**: Utiliza a técnica de Retrieval-Augmented Generation para compor respostas baseadas em contexto e documentos relevantes.
- **WebBaseLoader**: Carrega e processa documentos da web para enriquecer o conhecimento do agente.
- **Chroma Vector Store**: Armazena vetores de documentos para recuperação eficiente de informações relevantes.
- **Lambda Function**: Implementação de uma função AWS Lambda para servir como endpoint da API.

#### Exemplo de uso com .http:

POST http://api-travelagent-1723464635.us-east-2.elb.amazonaws.com
Content-Type: application/json

{
	"question": "Vou viajar para Londres em agosto de 2024. Quero que faça um roteiro de viagem para mim com eventos que irão ocorrer na data da viagem e com preço de passagens saindo de São Paulo para Londres. Também quero saber restaurantes, pontos turísticos e eventos culturais que ocorrerão na data da viagem."
}


RESPOSTA:

{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"message\": \"success\", \"details\": \"Para a sua viagem para Londres em agosto de 2024, preparei um roteiro completo com eventos, preços de passagens, opções de restaurantes, pontos turísticos e eventos culturais. Confira abaixo:\\n\\n**Roteiro de Viagem para Londres em Agosto de 2024:**\\n\\n1. **Eventos:**\\n   - Notting Hill Carnival\\n   - BBC Proms\\n   - Greenwich Music Time\\n   - London Craft Beer Festival\\n\\n2. **Preços de Passagens:**\\n   - Os preços das passagens de ida e volta de São Paulo para Londres em agosto de 2024 variam, mas começam a partir de £598.\\n\\n3. **Restaurantes:**\\n   - Explore os diversos restaurantes em Londres e aproveite a vibrante cena gastronômica da cidade. Alguns recomendados são:\\n     - The Ledbury\\n     - Sketch\\n     - Dishoom\\n     - Duck & Waffle\\n     - Hawksmoor\\n\\n4. **Pontos Turísticos:**\\n   - London Eye\\n   - Tower of London\\n   - Buckingham Palace\\n   - British Museum\\n   - Westminster Abbey\\n\\n5. **Eventos Culturais:**\\n   - Além dos eventos mencionados, aproveite para explorar a rica cena cultural de Londres, que inclui peças de teatro no West End, exposições em museus e galerias de arte, e concertos em locais históricos.\\n\\nEspero que este roteiro ajude a planejar uma viagem inesquecível para Londres em agosto de 2024. Aproveite ao máximo sua estadia na capital britânica!\"}"
}


#### Como Usar:

1. **Configuração de Ambiente**:
   - Configure a variável de ambiente `OPEN_API_KEY` com sua chave de API OpenAI.

2. **Endpoints Disponíveis**:
   - `POST http://api-travelagent-0.us-east-2.elb.amazonaws.com` O ENDPOINT FOI ALTERADO PARA EVITAR USO EXCESSIVO DA API E CONSUMO DO GPT. 
   - Payload esperado:
     ```json
     {
       "question": "Vou viajar para Londres em agosto de 2024. Quero que faça um roteiro de viagem para mim com eventos que irão ocorrer na data da viagem e com preço de passagens saindo de São Paulo para Londres. Também quero saber restaurantes, pontos turísticos e eventos culturais que ocorrerão na data da viagem."
     }
     ```

3. **Teste Local**:
   - Execute localmente python travelAgent.py.

4. **Deploy no Docker e AWS**:
   - Dockerize o projeto e faça o deploy na AWS ECS (Elastic Container Service) para disponibilizar o serviço como uma API escalável.

#### Dependências:

- Python 3.x
- `langchain-openai`, `langchain-community`, `langchain`, `beautifulsoup4`, `bs4`, `requests`, entre outras bibliotecas Python listadas no código.

