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
import json  
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
        print("file got")

        # Extract PDF text
        pdf_text = get_pdf_text(os.path.join(fs.location, filename))
        print("pdf text")

        # Integrate with OpenAI to create a book description
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "This following snippets are from a book. I need you to give me the author of the book, a description of the book in 100 characters, and the name of the book. I want you to give me these in the following format:{ name: "", description: "", author: ""} Only give your response in this format and don't add any more information."},
                {"role": "user", "content": pdf_text}
            ]
        )
        ai_response = response.choices[0].message['content']
        print(ai_response)

        # Parse AI response from string to dictionary
        try:
            book_data = json.loads(ai_response)
            print("book data here")

        except json.JSONDecodeError:
            # Handle the error if the response is not a valid JSON
            return render(request, 'home.html', {'error': 'Invalid AI response format'})

        # Add the book to the database
        embedder.add_book(book_data)
        print("embedded")

        return render(request, 'home.html', {'uploaded_file_url': uploaded_file_url, 'pdf_text': pdf_text, 'ai_description': ai_response})
    return render(request, 'home.html')

def home(request):
    return render(request, 'home.html')
