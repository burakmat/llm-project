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
                messages=[{"role": "user", "content": user_input}]
            )
            ai_response = response.choices[0].message['content']
            return JsonResponse({'response': ai_response})
        except Exception as e:
            return JsonResponse({'response': str(e)})

    return JsonResponse({'response': 'Invalid request'}, status=400)

def home(request):
    return render(request, 'home.html')
