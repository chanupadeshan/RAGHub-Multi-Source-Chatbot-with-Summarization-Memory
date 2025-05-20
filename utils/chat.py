from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.schema.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("API key is required")


def create_chat_chain(Model, docs):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    text = splitter.split_documents(docs)

    # Using HuggingFace embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_documents(text, embeddings)
    retriever = db.as_retriever()

    # Updated memory configuration
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key="answer"
    )

    llm = ChatGroq(
        groq_api_key=groq_api_key,
        model_name=Model,
        temperature=0.5
    )

    prompt = PromptTemplate(
        template="""You are a helpful assistant answering questions based on the provided content. 
        Provide clear, direct answers without showing your thinking process or analysis steps.
        
        Context: {context}
        Chat History: {chat_history}
        Question: {question}
        
        Answer the question directly and concisely:""",
        input_variables=["context", "chat_history", "question"]
    )

    chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        return_source_documents=True,
        combine_docs_chain_kwargs={"prompt": prompt}
    )

    return chain


