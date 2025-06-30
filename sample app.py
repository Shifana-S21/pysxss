from flask import Flask, request, render_template_string

app = Flask(__name__)

def simple_waf_filter(input_data):
    if input_data:
        blacklist = ["<script", "alert", "onerror"]
        
        print(f"[WAF] Input before filtering: {input_data}")
        
        for item in blacklist:
            if item in input_data.lower():
                input_data = input_data.replace(item, "")
                print(f"[WAF] Filtered out '{item}'")
        
        print(f"[WAF] Input after filtering: {input_data}")
    return input_data

@app.route('/')
def home():
    return """
    <h1>Welcome to the Vulnerable Test App</h1>
    <p>This application is designed to test XSS payloads against a simple WAF.</p>
    <p>Try to get an alert box to pop up using the search page.</p>
    <a href="/search?query=test">Go to the search page</a>
    """

@app.route('/search')
def search():
    query = request.args.get('query', '')
    
    safe_query = simple_waf_filter(query)
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Search Results</title>
    </head>
    <body>
        <h1>Search Results for: {safe_query}</h1>
        <p>Your query was reflected here.</p>
        <hr>
        <p>Try modifying the 'query' parameter in the URL.</p>
        <p>Example: <code>/search?query=<script>alert(1)</script></code> (this will be blocked)</p>
    </body>
    </html>
    """
    
    return render_template_string(html_template)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
