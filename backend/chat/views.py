from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import openai
import json
import os

@csrf_exempt
def chat_with_openai(request):
    if request.method == 'POST':
        user_input = request.POST.get('message', '')

        openai.api_key = settings.OPENAI_API_KEY # "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"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": "Create a book description based on the user message to enhance the accuracy of our book database's vector search. The goal is to help users find books that closely match their preferences. The format should effectively capture the key elements of the user message, enabling the database to align users with books that suit their tastes. Ensure the book description conveys the essence of the user message, allowing for a more precise search. Provide the book description only, without any additional information."},
                        {"role": "user", "content": user_input}]
            )
            ai_response = response.choices[0].message['content']
            return JsonResponse({'response': ai_response})
        except Exception as e:
            return JsonResponse({'response': str(e)})

    return JsonResponse({'response': 'Invalid request'}, status=400)

def home(request):
    return render(request, 'home.html')
