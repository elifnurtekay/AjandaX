from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
import json
from django.shortcuts import render

@csrf_exempt
def chat_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get("message", "")
        # LLM API’ye gönder
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct:free",  # ücretsiz ve iyi!
                "messages": [
                    {"role": "user", "content": message}
                ],
                "max_tokens": 128
            }
        )
        reply = response.json()["choices"][0]["message"]["content"]
        return JsonResponse({"reply": reply})
    return JsonResponse({"error": "Sadece POST!"}, status=405)

def chatbot_page(request):
    return render(request, "chatbot/chatbot.html")