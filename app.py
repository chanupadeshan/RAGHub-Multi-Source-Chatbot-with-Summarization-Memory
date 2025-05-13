import streamlit as st
from utils.extractors import load_pdf,load_url,load_YouTubeurl
from utils.summary import generate_summary
from utils.chat import create_chat_chain



st.set_page_config(page_title="Multi-Source Rag",layout="centered", page_icon=":robot:")
st.title("📚 Multi-Source chatbot with summary ")

API_KEY = st.sidebar.text_input("Enter your OpenAI API key", type="password", placeholder="sk-###")
Model = st.sidebar.selectbox("select Model:",("gpt-3.5-turbo","gpt-4","gpt-4-turbo"))
option= st.sidebar.selectbox("choose input type: ", ("Select Option","PDF","Website URL","YouTube URL"))

st.markdown("-----------------------------------------------------------")

if option == "PDF":
    st.header("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type = "pdf")
    if uploaded_file:
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.read())
        docs = load_pdf("temp.pdf")


elif option == "Website URL":
    st.header("Enter Website URL")
    uploaded_url = st.text_input("Enter the URL of the website",placeholder="https://example.com")
    if uploaded_url:
        docs = load_url(uploaded_url)


elif option == "YouTube URL":
    st.header("Enter YouTube URL")
    uploaded_YouTube_URL = st.text_input("Enter the URL of the YouTube video",placeholder="https://www.youtube.com/watch?v=example")
    if uploaded_YouTube_URL:
        docs = load_YouTubeurl(uploaded_YouTube_URL)

else:
    st.warning("Please select an option from the sidebar.")


if docs:
    st.success("Document loaded successfully!")
    summary = generate_summary(API_KEY,Model,docs)
    st.subheader("Summary:")
    st.write(summary)
    st.markdown("-----------------------------------------------------------")

    st.subheader("Chat With the Conetent:")
    chat_chain = create_chat_chain(API_KEY,Model,docs)


    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []


    user_input = st.text_input("Ask a question about the content:")
    if user_input:
        result = chat_chain.invoke({"question": user_input})
        st.session_state.chat_history.append(("You", user_input))
        st.session_state.chat_history.append(("Bot", result['answer']))

    for role, msg in st.session_state.chat_history:
        st.chat_message(role).write(msg)
