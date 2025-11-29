from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

class Store():

    def __init__(self , embedding_model):
        self.hf_embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        self.google_embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        if embedding_model == "models/gemini-embedding-001":
            self.embeddings = self.google_embeddings
        else:
            self.embeddings = self.hf_embeddings
                
    def create_vector_db(self , documents):
        if self.embeddings == self.hf_embeddings:
            hf_vectorstore = Chroma.from_documents(documents=documents , embedding=self.embeddings , persist_directory="hf_Chroma_Store")
            return hf_vectorstore
        elif self.embeddings == self.google_embeddings:
            google_vectorstore = Chroma.from_documents(documents=documents , embedding=self.google_embeddings , persist_directory="Chroma_Store")
            return google_vectorstore
    
    def create_retriever(self , vectorstore):
        retriever = vectorstore.as_retriever( search_type="similarity" ,search_kwargs={"k":3})
        return retriever
    