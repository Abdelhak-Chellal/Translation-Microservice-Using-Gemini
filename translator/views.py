# translator/views.py
from django.http import JsonResponse
from .gemini import translate_title

def test_translation(request):
    result = translate_title("Hello world")
    return JsonResponse({"translated": result})
