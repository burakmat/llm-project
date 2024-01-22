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

        openai.api_key = "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"

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": "Convert the user message into a book description format to enhance the accuracy of vector search on our book database. The goal is to provide users with books that match their preferences more precisely. Please ensure that the book description format captures the essence of the user message, allowing for a more accurate search. The format should effectively convey the key elements of the user message in a way that enables the database to match users with books that align with their preferences."},
                        {"role": "user", "content": user_input}]
            )
            ai_response = response.choices[0].message['content']
            return JsonResponse({'response': ai_response})
        except Exception as e:
            return JsonResponse({'response': str(e)})

    return JsonResponse({'response': 'Invalid request'}, status=400)

def home(request):
    return render(request, 'home.html')
