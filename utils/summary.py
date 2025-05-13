from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI



def generate_summary(API_KEY, Model, docs):
    if not API_KEY:
        raise ValueError("API key is required")
    if not docs:
        return "No content to summarize"
        
    try:
        llm = ChatOpenAI(openai_api_key=API_KEY, model_name=Model, temperature=0)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        text = text_splitter.split_documents(docs)
        chain = load_summarize_chain(llm, chain_type="map_reduce", verbose=True)
        summary = chain.run(text)
        return summary
    except Exception as e:
        raise Exception(f"Error generating summary: {str(e)}")