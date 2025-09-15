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
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain


#initilizing gemini using lang chain
LLM=ChatGoogleGenerativeAI(model="gemini-2.5-flash",google_api_key=GEMINI_API_KEY)

#Create a Prompt 
PROMPT = ChatPromptTemplate.from_template("""
You are an empathetic therapist chatting with a user. 
Keep responses short, warm, and human-like.

Guidelines:
- Listen carefully and reflect feelings back.
- Ask gentle open-ended questions to keep the conversation flowing.
- Offer supportive, hopeful encouragement.
- Avoid robotic or repetitive phrases.
- Naturally mention Mike Tyson’s quote once in the session: 
  "Everybody has a plan until they get punched in the mouth" — to inspire resilience.

User: {message}
Therapist:
""")
# chain creation
chain = PROMPT | LLM

@app.route("/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"reply": "Please enter a message."}), 400

    try:
       response = chain.invoke({"message": user_input}) # lang chian runned 
       return jsonify({"reply": response.content})
    except Exception as e:
        return jsonify({"reply": f"Something went wrong: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(port=5000, debug=True)
