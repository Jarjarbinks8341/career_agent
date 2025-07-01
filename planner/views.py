from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import PyPDF2
import io
import openai
import os

# Create your views here.

class CVSuggestionView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file uploaded.'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            pdf_reader = PyPDF2.PdfReader(file_obj)
            text = "\n".join(page.extract_text() or '' for page in pdf_reader.pages)
        except Exception as e:
            return Response({'error': f'Failed to read PDF: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        # Call OpenAI GPT API
        openai.api_key = os.getenv("OPENAI_API_KEY")
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a career advisor."},
                    {"role": "user", "content": f"My CV: {text}\nWhat career path do you suggest for me?"}
                ],
                max_tokens=300,
                temperature=0.7,
            )
            suggestion = response.choices[0].message["content"]
        except Exception as e:
            return Response({'error': f'Failed to get suggestion from GPT: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'suggestion': suggestion})
