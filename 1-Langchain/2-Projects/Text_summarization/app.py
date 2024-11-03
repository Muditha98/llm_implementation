import yt_dlp
import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain.schema import Document
from langchain_community.document_loaders import UnstructuredURLLoader

def load_youtube_video_text(url):
    # Use yt-dlp to extract video information and transcript
    ydl_opts = {
        'quiet': True,
        'format': 'bestaudio/best',
        'skip_download': True,
        'noplaylist': True,
        'writesubtitles': True,
        'subtitleslangs': ['en'],
        'writeautomaticsub': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        title = info.get("title", "Unknown Title")
        description = info.get("description", "")
        return title, description

## Streamlit app
st.set_page_config(page_title="Langchain: Summarize Text from YouTube or Websites")
st.title("Langchain: Summarize text from Youtube or Websites")
st.subheader("Summarize URL")

## Get the GROQ API key and URL (YouTube or website) to be summarized
with st.sidebar:
    groq_api_key = st.text_input("Groq groq_api_key", value="", type="password")

generic_url = st.text_input("URL", label_visibility="collapsed")

## Gemma model using Groq API 
llm = ChatGroq(model="Gemma-7b-It", groq_api_key=groq_api_key)

prompt_template = """
Provide summary of the following content in 300 words:
Content: {text}
"""

prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

if st.button("Summarize the content from YouTube or Website"):
    ## Validate all the inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")

    elif not validators.url(generic_url):
        st.error("Please enter a valid URL. It can be a YouTube video URL or Website URL")

    else:
        try:
            with st.spinner("Waiting..."):
                ## Loading the website or YouTube video data
                if "youtube.com" in generic_url:
                    title, description = load_youtube_video_text(generic_url)
                    content = f"Title: {title}\nDescription: {description}"
                    docs = [Document(page_content=content)]
                else:
                    loader = UnstructuredURLLoader(
                        urls=[generic_url],
                        ssl_verify=False,
                        headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                        }
                    )
                    docs = loader.load()

                ## Chain for summarization
                chain = load_summarize_chain(llm, chain_type="stuff", prompt=prompt)
                output_summary = chain.run(docs)

                st.success(output_summary)

        except Exception as e:
            st.exception(f"Exception: {e}")
