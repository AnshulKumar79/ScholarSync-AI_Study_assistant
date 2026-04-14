# import os
# import google.generativeai as genai
# from dotenv import load_dotenv

# # .env se key load karein
# load_dotenv()

# # GenAI configure karein
# api_key = os.getenv("GEMINI_API_KEY")
# genai.configure(api_key=api_key)

# print("Aapke liye available models ki list:\n")
# # Sabhi models ko list karein jo text generation support karte hain
# for m in genai.list_models():
#     if 'generateContent' in m.supported_generation_methods:
#         print(m.name)



import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

print("Available Embedding models ki list:\n")
for m in genai.list_models():
    # Is baar hum embedContent support check kar rahe hain
    if 'embedContent' in m.supported_generation_methods:
        print(m.name)