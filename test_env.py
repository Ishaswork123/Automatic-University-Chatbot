import os
from dotenv import load_dotenv
from groq import Groq

# 1. Load the .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("❌ Error: GROQ_API_KEY not found in .env file.")
    exit(1)

try:
    # 2. Initialize Groq client
    client = Groq(api_key=api_key)
    
    # 3. Simple ping/test request
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Hello, respond with 'Pong' only.",
            }
        ],
        model="llama-3.3-70b-versatile",
    )
    
    response_text = chat_completion.choices[0].message.content.strip()
    
    if "Pong" in response_text:
        print("✅ Environment Secure and Working")
    else:
        print(f"⚠️ Connection successful, but unexpected response: {response_text}")

except Exception as e:
    print(f"❌ Failed: {str(e)}")
