from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

def generate_summary(Model, docs):
    if not groq_api_key:
        raise ValueError("API key is required")
    if not docs:
        return "No content to summarize"
    
    try:
        llm = ChatGroq(
            groq_api_key=groq_api_key,
            model_name=Model,
            temperature=0.5,
            verbose=False
        )

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        text_chunks = text_splitter.split_documents(docs)[:20] 
        # Create a prompt that explicitly asks for a clean summary without thinking process
        prompt = PromptTemplate(
            template="""Write a clear and concise summary of the following text. Do not include any thinking process, analysis steps, or meta-commentary. Just provide the final summary:{text}""",
            input_variables=["text"]
        )

        chain = load_summarize_chain(
            llm, 
            chain_type="stuff", 
            verbose=True,
            prompt=prompt
        )
        
        summary = chain.run(text_chunks)
        
        # Clean up the summary
        if summary:
            # Remove any thinking process markers
            summary = summary.replace("<think>", "").replace("</think>", "")
            # Remove any "Summary:" prefixes
            summary = summary.replace("Summary:", "").strip()
            
        return summary.strip()
        
    except Exception as e:
        raise Exception(f"Error generating summary: {str(e)}")
