from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.db import connection

def vulnerable_view(request):
    query = request.GET.get('query', '')
    # UNSAFE RAW QUERY (INTENTIONALLY VULNERABLE)
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM vuln_app_artist WHERE name = '{query}'")
        results = cursor.fetchall()
    return HttpResponse(f"Results: {results}")