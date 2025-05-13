from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate
from langchain.schema.messages import HumanMessage, SystemMessage


def create_chat_chain(API_KEY,Model,docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000,chunk_overlap=200)
    text = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=API_KEY)
    db = FAISS.from_documents(text,embeddings)
    retriever = db.as_retriever()


    memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)
    llm = OpenAI(openai_api_key=API_KEY,model_name=Model,temperature=0.5)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system","You are a helpful assistant answering questions based on the provided content."),
            ("human","{question}")
        ]
    )


    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt":prompt}
    )


    return chain