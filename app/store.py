from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

class Store():
    
    def __init__(self):
        self.hf_embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.google_embedding = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
    
    def create_vector_store(self , documents , embeddings , directory):
        vector_store = Chroma.from_documents(documents=documents , embedding=embeddings , persist_directory=directory)
        return vector_store
    
    def create_retriever(self ,vectorstore):
        retriever = vectorstore.as_retriever(search_type="similarity" , search_kwargs={"k":3})
        return retriever
    