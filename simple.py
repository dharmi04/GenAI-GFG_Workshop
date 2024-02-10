import google.generativeai as genai
import os
import dotenv


dotenv.load_dotenv()


gemini_api_key = os.getenv("GOOGLE_GEMINI_AI")
genai.configure(api_key = gemini_api_key)


prompot = input("Enter your question: ")


model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(prompot)


print(response.text)
