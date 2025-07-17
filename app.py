from flask import Flask, request, Response
import requests
import os

app = Flask(__name__)

@app.route('/proxy')
def proxy():
    target_url = request.args.get('url')
    if not target_url:
        return 'Missing URL', 400

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0 Safari/537.36',
            'Referer': target_url,
            'Origin': target_url,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        }

        resp = requests.get(target_url, headers=headers, stream=True)

        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding',
                            'connection', 'x-frame-options', 'content-security-policy']

        response_headers = [(name, value) for (name, value) in resp.raw.headers.items()
                            if name.lower() not in excluded_headers]

        return Response(resp.content, resp.status_code, response_headers)

    except Exception as e:
        return f'Error: {str(e)}', 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
