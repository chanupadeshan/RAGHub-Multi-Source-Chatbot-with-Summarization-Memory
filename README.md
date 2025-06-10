# Multi-Source RAG Chatbot with Summarization & Memory

A powerful Streamlit-based chatbot application that can process multiple types of content sources (PDFs, websites, and YouTube videos) using RAG (Retrieval-Augmented Generation) technology. The application provides content summarization and interactive chat capabilities powered by advanced language models.

## Features

- **Multi-Source Support**:
  - PDF document processing
  - Website content extraction
  - YouTube video transcription and processing

- **Advanced Language Models**:
  - Support for multiple LLM options:
    - Qwen QWQ 32B
    - DeepSeek R1 Distill LLaMA 70B

- **Key Functionalities**:
  - Automatic content summarization
  - Interactive chat interface
  - Persistent chat history
  - Clean and intuitive user interface

## Prerequisites

- Python 3.8 or higher
- Groq API key
- Required Python packages (listed in requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided local URL (typically http://localhost:8501)

3. Using the Application:
   - Select your preferred language model from the sidebar
   - Choose your input type (PDF, Website URL, or YouTube URL)
   - Upload or input your content
   - Wait for the content to be processed and summarized
   - Start chatting with the content using the chat interface

## Input Types

### PDF Documents
- Upload PDF files directly through the interface
- The application will process and chunk the content for analysis

### Website URLs
- Enter any website URL
- The application will extract and process the content

### YouTube Videos
- Provide a YouTube video URL
- The application will transcribe and process the video content

## Features in Detail

### Content Summarization
- Automatic generation of comprehensive summaries
- Processing time varies based on content size
- Clear presentation of summarized content

### Chat Interface
- Interactive chat system
- Persistent chat history
- Real-time responses
- Clean and formatted output

## Error Handling
The application includes comprehensive error handling for:
- Invalid file uploads
- Unreachable URLs
- Processing errors
- API connection issues

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.



## Acknowledgments
- Streamlit for the web application framework
- Groq for the language model API
- All other open-source libraries used in this project
