import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv 

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY") 

app = Flask(__name__)
CORS(app)

#for chain
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader



#initilizing gemini using lang chain
LLM=ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=GEMINI_API_KEY,temperature=0.7)

#load  data
loader = TextLoader("backend/therapy_notes.txt")   
docs = loader.load()

#embedings
# --- Hugging Face embeddings instead of Gemini ---
from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


 #create a embedding model. chunks to vector
vector_store=FAISS.from_documents(docs,embeddings) # model, converts all docs into vectors, and stores them in a FAISS vector databas
retriever = vector_store.as_retriever(search_kwargs={"k": 3}) # database to retriver object find top k most relevant document



#Create a Prompt 
PROMPT = PromptTemplate(
    template="""
You are an empathetic therapist chatting with a user. 
Keep responses short, warm, and human-like.

Guidelines:
- Listen carefully and reflect feelings back.
- Ask gentle open-ended questions to keep the conversation flowing.
- Offer supportive, hopeful encouragement.
- Avoid robotic or repetitive phrases.
- Naturally mention Mike Tyson’s quote once in the session:     
  "Everybody has a plan until they get punched in the mouth" — to inspire resilience.

Context:
{context}

User: {question}
Therapist:""",
    input_variables=["context", "question"],
)

# chain for retrival qa
chain = RetrievalQA.from_chain_type(
    llm=LLM,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": PROMPT}
)

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"reply": "Please enter a message."}), 400

    try:
       response = chain.invoke({"query": user_input}) # lang chian runned 
       return jsonify({"reply": response["result"]})
    except Exception as e:
        return jsonify({"reply": f"Something went wrong: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
