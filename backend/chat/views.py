from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import openai
from chat.apps import embedder
import os
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from pdf_reader import get_pdf_text

@csrf_exempt
def chat_with_openai(request):
    if request.method == 'POST':
        user_input = request.POST.get('message', '')

        openai.api_key = settings.OPENAI_API_KEY

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Create a book description based on the user message to enhance the accuracy of our book database's vector search."},
                    {"role": "user", "content": user_input}
                ]
            )
            ai_response = response.choices[0].message['content']

            # Use the Embedder to query books based on AI response
            book_hits = embedder.query_books(ai_response)
            print(book_hits)
            # Format the response data
            formatted_hits = [{'payload': hit.payload, 'score': hit.score} for hit in book_hits]
            
            return JsonResponse({'book_hits': formatted_hits})
        except Exception as e:
            return JsonResponse({'response': str(e)})

    return JsonResponse({'response': 'Invalid request'}, status=400)



def upload_file(request):
    if request.method == 'POST' and request.FILES['file-input']:
        myfile = request.FILES['file-input']
        fs = FileSystemStorage(location=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = filename
        return render(request, 'home.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'home.html')


def home(request):
    return render(request, 'home.html')
