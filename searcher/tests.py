import json
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from django.conf import settings
 
class SearcherTests(TestCase):
    def setUp(self):
        self.client = Client()
 
    @patch('searcher.views.requests.get')
    def test_search_and_csv_download(self, mock_get):
        sample_api_response = {
            "organic_results": [
                {"title": "Result 1", "link": "https://example.com/1", "snippet": "Snippet 1"},
                {"title": "Result 2", "link": "https://example.com/2", "snippet": "Snippet 2"},
            ]
        }
        mock_resp = mock_get.return_value
        mock_resp.status_code = 200
        mock_resp.json.return_value = sample_api_response
 
        # Post a search
        post_data = {'queries': "python testing\ndjango unit test"}
        response = self.client.post(reverse('index'), post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        # Check that results appear in context
        self.assertContains(response, "Result 1")
        self.assertContains(response, "example.com/1")
 
        # Now test CSV download uses session data
        download_resp = self.client.get(reverse('download_csv'))
        self.assertEqual(download_resp.status_code, 200)
        self.assertEqual(download_resp['Content-Type'], 'text/csv')
        content = download_resp.content.decode()
        # Should contain headers and at least one row
        self.assertIn("query,title,link,snippet", content)
        self.assertIn("python testing", content)
        self.assertIn("Result 1", content)
 
    @patch('searcher.views.requests.get')
    def test_api_error_handling(self, mock_get):
        mock_resp = mock_get.return_value
        mock_resp.status_code = 500
        mock_resp.text = "Internal Error"
        mock_resp.json.return_value = {}
 
        post_data = {'queries': "something"}
        response = self.client.post(reverse('index'), post_data, follow=True)
        self.assertContains(response, "ValueSERP API error", status_code=200)