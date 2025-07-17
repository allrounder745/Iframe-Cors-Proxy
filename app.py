from flask import Flask, request, Response
import requests

app = Flask(__name__)

@app.route('/proxy')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return 'Missing URL', 400

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }
        resp = requests.get(target_url, headers=headers)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 
                            'connection', 'x-frame-options', 'content-security-policy']

        # Strip problematic headers
        response_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                            if name.lower() not in excluded_headers]

        # Return raw HTML
        return Response(resp.content, resp.status_code, response_headers)
    except Exception as e:
        return str(e), 500
