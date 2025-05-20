import streamlit as st
from utils.extractors import load_pdf,load_url,load_YouTubeurl
from utils.summary import generate_summary
from utils.chat import create_chat_chain
from utils.clean_response import clean_response
import os
from dotenv import load_dotenv

# Set page config first
st.set_page_config(page_title="Multi-Source Rag",layout="centered", page_icon=":robot:")

# Load environment variables
load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("Please set your GROQ_API_KEY in the .env file")
    st.stop()

# Initialize docs as None
docs = None

st.title("📚 Multi-Source chatbot with summary ")

Model = st.sidebar.selectbox("Select Model:",("qwen-qwq-32b","deepseek-r1-distill-llama-70b"))
option= st.sidebar.selectbox("choose input type: ", ("Select Option","PDF","Website URL","YouTube URL"))

st.markdown("-----------------------------------------------------------")

if option == "PDF":
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type = "pdf")
    if uploaded_file:
        try:
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.read())
            docs = load_pdf("temp.pdf")
            st.write(f"Number of pages loaded: {len(docs)}")
        except Exception as e:
            st.error(f"Error loading PDF: {str(e)}")

elif option == "Website URL":
    st.header("Enter Website URL")
    uploaded_url = st.text_input("Enter the URL of the website",placeholder="https://example.com")
    if uploaded_url:
        try:
            docs = load_url(uploaded_url)
            st.write(f"Number of chunks loaded: {len(docs)}")
        except Exception as e:
            st.error(f"Error loading URL: {str(e)}")

elif option == "YouTube URL":
    st.header("Enter YouTube URL")
    uploaded_YouTube_URL = st.text_input("Enter the URL of the YouTube video",placeholder="https://www.youtube.com/watch?v=example")
    if uploaded_YouTube_URL:
        try:
            docs = load_YouTubeurl(uploaded_YouTube_URL)
            st.write(f"Number of chunks loaded: {len(docs)}")
        except Exception as e:
            st.error(f"Error loading YouTube video: {str(e)}")

else:
    st.warning("Please select an option from the sidebar.")

if docs:
    try:
        st.success("Document loaded successfully!")
        
        with st.spinner("Generating summary... This may take a few minutes depending on the document size."):
            summary = generate_summary(Model, docs)
            
        st.subheader("Summary:")
        st.write(summary)
        st.markdown("-----------------------------------------------------------")

        st.subheader("Chat With the Content:")
        with st.spinner("Initializing chat system..."):
            chat_chain = create_chat_chain(Model, docs)

        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        # Show chat messages first
        for role, msg in st.session_state.chat_history:
            if role == "You":
                st.chat_message("user").write(msg)
            else:
                st.chat_message("assistant").write(msg)

        # Input field at the bottom
        if "user_input" not in st.session_state:
            st.session_state.user_input = ""

        user_input = st.text_input("Ask a question about the content:", key="user_input")

        if user_input:
            st.write("Processing your question...")
            result = chat_chain.invoke({"question": user_input})
            result = clean_response(result)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", result['answer']))
            
            # Clear input field after sending
            st.session_state.user_input = ""

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
