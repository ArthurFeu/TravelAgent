import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

# embeddings import
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableSequence
import bs4
import json

OPEN_API_KEY = os.environ.get("OPEN_API_KEY")

llm = ChatOpenAI(model="gpt-3.5-turbo")

# query = """
# Vou viajar para Londres em agosto de 2024. Quero que faça um roteiro de viagem para mim com eventos que irão ocorrer na data da viagem e com preço de passagens saindo de são paulo para londres. Também quero saber restaurantes, pontos turísticos e eventos culturais que ocorrerão na data da viagem.
# """

# Coletar respostas do agente de pesquisa pelo chat gpt + ddg-search + wikipedia
def research_agent(query, llm):
    tools = load_tools(["ddg-search", "wikipedia"], llm=llm)
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, prompt=prompt)
    web_context = agent_executor.invoke({"input": query})
    return web_context["output"]

# RAG agent - retrieval augmented generation
def load_data():
    # Corrigir a URL inválida e carregar os dados da web
    loader = WebBaseLoader(
        web_paths=["https://www.dicasdeviagem.com/inglaterra/"],
        bs_kwargs=dict(parse_only=bs4.SoupStrainer(class_=("postcontentwrap", "pagetitleloading background-imaged loading-dark")))
    )
    
    # Separar documento
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    
    vector_store = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
    retriever = vector_store.as_retriever()
    return retriever

def get_relevant_docs(query):
    retriever = load_data()
    relevant_docs = retriever.get_relevant_documents(query)
    return relevant_docs
    
def supervisor_agent(query, llm, web_context, relevant_docs):
    prompt_template = """
        Você é um gerente de uma agência de viagens. Sua resposta final deverá ser um roteiro de viagens completo e detalhado.
        Utilize o contexto de eventos e preços de passagens, o input do usuário e também os documentos relevantes para elaborar o roteiro.
        Contexto: {web_context}
        Documento relevante: {relevant_docs}
        Usuário: {query}
        Assistente:
    """

    prompt = PromptTemplate(
        input_variables=["web_context", "relevant_docs", "query"],
        template=prompt_template
    )
 
    sequence = RunnableSequence(prompt | llm)
 
    response = sequence.invoke({"web_context": web_context, "relevant_docs": relevant_docs, "query": query})
    return response

def get_response(query, llm):
    web_context = research_agent(query, llm)
    relevant_docs = get_relevant_docs(query)
    response = supervisor_agent(query, llm, web_context, relevant_docs)
    return response

def lambda_handler(event, context):
    body = json.loads(event.get('body', {}))
    query = body.get('question', 'Parametro question não encontrado')
    response = get_response(query, llm).content
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps({
            'message': 'success',
            'details': response,
        }),
    }

# Teste local
if __name__ == "__main__":
    test_event = {
        "body": json.dumps({
            "question": "Vou viajar para Londres em agosto de 2024. Quero que faça um roteiro de viagem para mim com eventos que irão ocorrer na data da viagem e com preço de passagens saindo de São Paulo para Londres. Também quero saber restaurantes, pontos turísticos e eventos culturais que ocorrerão na data da viagem."
        })
    }
    print(lambda_handler(test_event, None))