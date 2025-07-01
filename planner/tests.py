from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.

class CVSuggestionViewTest(APITestCase):
    def test_no_file_uploaded(self):
        url = reverse('cv-suggest')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_pdf_upload(self):
        url = reverse('cv-suggest')
        # Create a simple PDF in memory
        pdf_content = b'%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF'
        file = SimpleUploadedFile('test.pdf', pdf_content, content_type='application/pdf')
        response = self.client.post(url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('suggestion', response.data)
