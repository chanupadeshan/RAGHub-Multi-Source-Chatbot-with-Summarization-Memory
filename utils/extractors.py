from langchain.document_loaders import PyPDFLoader,WebBaseLoader
from langchain_community.document_loaders import YoutubeLoader
import os



def load_pdf(file):
    if not file or not os.path.exists(file):
        raise ValueError("Invalid PDF file")
    try:
        loader = PyPDFLoader(file)
        return loader.load()
    except Exception as e:
        raise Exception(f"Error loading PDF: {str(e)}")

def load_url(url):
    if not url or not url.startswith(('http://', 'https://')):
        raise ValueError("Invalid URL")
    try:
        loader = WebBaseLoader(url)
        return loader.load()
    except Exception as e:
        raise Exception(f"Error loading URL: {str(e)}")

def load_YouTubeurl(url):
    if not url or 'youtube.com' not in url and 'youtu.be' not in url:
        raise ValueError("Invalid YouTube URL")
    try:
        loader = YoutubeLoader.from_youtube_url(url)
        return loader.load()
    except Exception as e:
        raise Exception(f"Error loading YouTube video: {str(e)}")