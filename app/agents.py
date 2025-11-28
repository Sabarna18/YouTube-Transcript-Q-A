from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class Agent():
    
    def __init__(self):
        self.groq_model = ChatGroq(model="llama-3.3-70b-versatile" , temperature=0.5 , max_tokens=3000)
        self.google_llm = init_chat_model("google_genai:gemini-2.5-flash" , temperature=0.5)
        
    def format_docs(self , docs):
        formatted = "\n\n".join(doc.page_content for doc in docs)
        return formatted
    
    def generate_answer(self , retriever , model , question):
        template = '''
            you are video transcript analyser. the transcript is provided as context and based on the context 
            answer the following questions asked by user. Answer 'I don't know' if the question is out of context.
            context : {context},
            question : {question}
        '''
        prompt = PromptTemplate.from_template(template)
        rag_chain = (
            {"context": retriever | self.format_docs , "question": RunnablePassthrough()}
            | prompt
            | model   
            | StrOutputParser()       
        )
        answer = rag_chain.invoke(question)
        return answer