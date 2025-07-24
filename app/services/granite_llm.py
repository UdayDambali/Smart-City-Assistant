# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# API_KEY = os.getenv("WATSONX_API_KEY")
# PROJECT_ID = os.getenv("PROJECT_ID")
# MODEL_ID = os.getenv("MODEL_ID")

# def generate_chat_response(prompt: str):
#     url = f"https://us-south.ml.cloud.ibm.com/ml/v1/text-generation/{PROJECT_ID}/generate"
#     headers = {
#         "Authorization": f"Bearer {API_KEY}",
#         "Content-Type": "application/json"
#     }
#     payload = {
#         "model_id": MODEL_ID,
#         "inputs": [prompt],
#         "parameters": {
#             "max_new_tokens": 256,
#             "temperature": 0.7
#         }
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     return response.json()

from app.core.config import settings
from ibm_watsonx_ai import APIClient, Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

credentials = Credentials(
    url = "https://eu-gb.ml.cloud.ibm.com",
    api_key = settings.WATSONX_API_KEY,
)

client = APIClient(credentials)

model = ModelInference(
  model_id=settings.MODEL_ID,
  api_client=client,
  project_id=settings.PROJECT_ID,
  params = {
      "max_new_tokens": 100,
      "temperature": 0.3  # Lowered for more factual answers
  }
)

def generate_chat_response(prompt: str, chat_history=None):
    """
    Generate a response using the LLM, with optional chat history for context.
    """
    system_prompt = (
        "You are a helpful and factual smart city assistant. "
        "Answer questions concisely and accurately. "
        "If you don't know the answer, say so.\n"
    )
    # If chat_history is provided, prepend it as context
    history_text = ""
    if chat_history:
        for sender, message in chat_history:
            if sender == "user":
                history_text += f"User: {message}\n"
            else:
                history_text += f"Assistant: {message}\n"
    full_prompt = system_prompt + history_text + f"User: {prompt}\nAssistant:"
    response = model.generate_text(full_prompt)
    return response

