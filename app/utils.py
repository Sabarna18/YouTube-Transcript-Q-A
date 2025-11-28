from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import WebshareProxyConfig
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import time
import random



def extract_transcript(url):
    video_id = url.split('v=')[1].split("&")[0]
    ytt_api = YouTubeTranscriptApi()
    raw_trans = ytt_api.fetch(video_id , languages=['hi' , 'en'])
    trans_list = raw_trans.snippets
    final_transcript = ""
    for entry in trans_list:
        final_transcript = final_transcript + entry.text
    return final_transcript

def create_Documents(data):
    document = Document(
                page_content=data
            )
    return document

def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=3000 , chunk_overlap=200)
    chunks = text_splitter.split_documents([documents])
    return chunks

    