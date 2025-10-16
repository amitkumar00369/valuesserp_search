import csv
import io
import requests
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import MultiSearchForm
from django.views.decorators.http import require_http_methods
# from django.views.decorators.csrf import csrf_exempt  # csrf in templates present
from dotenv import load_dotenv
load_dotenv()
import os


VALUESERP_BASE  = os.getenv('base_url')
def call_valueserp(query):
    api_key = os.getenv("VALUESSERP_API_KEY")
    if not api_key:
        raise RuntimeError("API key missing (VALUESERP_API_KEY)")
    params = {"q": query, "api_key": api_key, "num": 10} 
    resp = requests.get(VALUESERP_BASE, params=params, timeout=10)
    if resp.status_code != 200:
        raise RuntimeError(f"ValueSERP API error: {resp.status_code} {resp.text}")
    data = resp.json()

    results = []
    organic = data.get("organic_results") or data.get("organic", []) or data.get("results") or []
    for item in organic:
        title = item.get("title") or item.get("name") or ""
        link = item.get("link") or item.get("url") or item.get("displayed_link") or ""
        snippet = item.get("snippet") or item.get("snippet_text") or item.get("description") or ""
        results.append({"title": title, "link": link, "snippet": snippet})
    return results
 
@require_http_methods(["GET", "POST"])
def index_view(request):
    context = {"error": None, "results": [], "queries_submitted": []}
    if request.method == "POST":
        form = MultiSearchForm(request.POST)
        if form.is_valid():
            queries = form.cleaned_data["queries"]
            session_results = []
            for q in queries:
                try:
                    api_results = call_valueserp(q)
                except Exception as e:
                    context["error"] = str(e)
                    api_results = []
          
                session_results.append({"query": q, "results": api_results})
            request.session["last_search_results"] = session_results
            context["results"] = session_results
            context["queries_submitted"] = queries
        else:
            context["error"] = form.errors.as_json()
    else:
        form = MultiSearchForm()
    return render(request, "searcher/index.html", context)
 
def download_csv(request):

    session_results = request.session.get("last_search_results")
    if not session_results:
        return HttpResponse("No search results in session to download.", status=400)
 
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["query", "title", "link", "snippet"])
    for block in session_results:
        query = block.get("query", "")
        for item in block.get("results", []):
            writer.writerow([query, item.get("title", ""), item.get("link", ""), item.get("snippet", "")])
 
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="valueserp_results.csv"'
    return response
 