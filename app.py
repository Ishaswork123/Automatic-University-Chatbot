from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__, static_folder='.')
CORS(app) 

# ---- Serve Website Files ----
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

# ---- Groq API Setup ----
GROQ_API_KEY = "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"
client = Groq(api_key=GROQ_API_KEY)

# Define the system prompt based on your website's focus (Britannia University)
# I have adapted your StanfordBot template to match your website's content.
SYSTEM_PROMPT = """
You are BritanniaBot — an AI assistant that ONLY provides information related to
Britannia University (located in Lahore, Pakistan). You help users with questions about:

• Admissions (Open twice a year for Undergrad, Grad, and PhD)
• Scholarships & Financial Aid
• Academics & Majors (CS, Business, Biotech, Social Sciences, IT)
• Programs & Departments
• Research
• Contact Information (Email: info@britannia.edu, Phone: +92-300-1234567)
• Campus life
• Campus location (Lahore, Pakistan)

RULES:
1. Only answer questions related to Britannia University.
2. If the question is not related to Britannia University, politely decline by saying:
   "I’m sorry, but I can only assist with information related to Britannia University."
3. Do NOT answer questions about other universities, general knowledge,
   programming, math, politics, religion, or personal advice.
4. Keep responses short, helpful, and friendly.
"""

def get_completion_from_messages(messages, model="llama-3.3-70b-versatile", temperature=0):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
    )
    return response.choices[0].message.content

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message")
    
    if not user_message:
        return jsonify({"reply": "No message received."}), 400

    # Prepare messages with system prompt
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message}
    ]

    try:
        bot_reply = get_completion_from_messages(messages)
        return jsonify({"reply": bot_reply})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"reply": "I'm having trouble connecting to my brain right now. Please try again later."}), 500

if __name__ == "__main__":
    # Ensure the server runs on port 5000 as expected by chatbot.js
    print("\n✅ Website is live at: http://127.0.0.1:5000")
    app.run(port=5000, debug=True)
