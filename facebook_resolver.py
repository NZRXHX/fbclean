#!/usr/bin/env python3
"""
Facebook Link Resolver - Backend API
Run: python3 facebook_resolver.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import re
import logging

app = Flask(__name__)
CORS(app)  # Allow frontend to call this API

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/resolve', methods=['POST', 'GET'])
def resolve_facebook_link():
    """Resolve a Facebook share URL to its final video URL"""
    
    if request.method == 'GET':
        url = request.args.get('url')
    else:
        data = request.get_json()
        url = data.get('url') if data else None
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    # Clean up the URL
    url = url.strip()
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url
    
    logger.info(f"Resolving: {url}")
    
    try:
        # Make the request with headers matching your curl command
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:154.0) Gecko/20100101 Firefox/154.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Connection': 'keep-alive',
        }
        
        # Use a session to handle cookies
        session = requests.Session()
        
        # First, try with HEAD to get the location header (like curl -I)
        response = session.head(url, headers=headers, allow_redirects=False, timeout=10)
        
        # Check if we got a redirect
        if response.status_code in [301, 302, 303, 307, 308]:
            location = response.headers.get('Location')
            if location:
                logger.info(f"Found redirect via HEAD: {location}")
                # Clean the URL (remove tracking params)
                clean_url = clean_facebook_url(location)
                return jsonify({
                    'success': True,
                    'original_url': url,
                    'resolved_url': location,
                    'clean_url': clean_url,
                    'method': 'HEAD_redirect'
                })
        
        # If HEAD didn't work, try GET and parse the HTML
        response = session.get(url, headers=headers, timeout=10)
        
        # Check if the response contains a redirect
        html = response.text
        
        # Look for meta refresh
        meta_match = re.search(r'<meta[^>]*http-equiv=["\']refresh["\'][^>]*content=["\']0;\s*URL=([^"\' ]+)[ "\']', html, re.I)
        if meta_match:
            location = meta_match.group(1)
            logger.info(f"Found redirect via meta refresh: {location}")
            clean_url = clean_facebook_url(location)
            return jsonify({
                'success': True,
                'original_url': url,
                'resolved_url': location,
                'clean_url': clean_url,
                'method': 'meta_refresh'
            })
        
        # Look for JavaScript redirect
        js_match = re.search(r'window\.location\.(?:href|replace)\s*=\s*["\']([^"\']+)["\']', html, re.I)
        if js_match:
            location = js_match.group(1)
            logger.info(f"Found redirect via JavaScript: {location}")
            clean_url = clean_facebook_url(location)
            return jsonify({
                'success': True,
                'original_url': url,
                'resolved_url': location,
                'clean_url': clean_url,
                'method': 'javascript_redirect'
            })
        
        # Look for any reel/video URL in the page
        video_match = re.search(r'(https://web\.facebook\.com/(?:reel|watch|videos?)/\d+)', html)
        if video_match:
            video_url = video_match.group(1)
            logger.info(f"Found video URL in page: {video_url}")
            return jsonify({
                'success': True,
                'original_url': url,
                'resolved_url': video_url,
                'clean_url': video_url,
                'method': 'page_scan'
            })
        
        # If we got here, no redirect found
        return jsonify({
            'success': False,
            'error': 'No redirect found. The URL might not be a Facebook share link or requires login.',
            'original_url': url,
            'status_code': response.status_code
        }), 404
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Request failed: {str(e)}'
        }), 500

def clean_facebook_url(url):
    """Remove tracking parameters from Facebook URLs"""
    # Split off query parameters
    if '?' in url:
        base = url.split('?')[0]
        return base
    return url

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'name': 'Facebook Link Resolver API',
        'endpoints': {
            '/resolve?url=YOUR_URL': 'GET - Resolve a Facebook share URL'
        },
        'example': '/resolve?url=https://web.facebook.com/share/r/19B8Zpc5yv/'
    })

if __name__ == '__main__':
    print("🚀 Facebook Link Resolver API running on http://localhost:5000")
    print("📝 Example: http://localhost:5000/resolve?url=https://web.facebook.com/share/r/19B8Zpc5yv/")
    app.run(host='0.0.0.0', port=5000, debug=True)
