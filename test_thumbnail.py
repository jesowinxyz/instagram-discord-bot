"""
Quick test script to verify Instagram thumbnail fetching works
"""
import requests
import re

def test_instagram_thumbnail(instagram_url):
    """Test all 3 methods of fetching Instagram thumbnails"""
    
    clean_url = instagram_url.rstrip('/').split('?')[0]
    print(f"\n🔍 Testing thumbnail fetch for: {clean_url}\n")
    
    # Method 1: Facebook Graph API
    print("Method 1: Facebook Graph oEmbed API")
    try:
        if '/reel/' in clean_url:
            oembed_url = clean_url.replace('/reel/', '/p/')
        elif '/tv/' in clean_url:
            oembed_url = clean_url.replace('/tv/', '/p/')
        else:
            oembed_url = clean_url
        
        api_url = f"https://graph.facebook.com/v12.0/instagram_oembed?url={oembed_url}&access_token=&fields=thumbnail_url"
        response = requests.get(api_url, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if 'thumbnail_url' in data:
                print(f"✅ SUCCESS! Thumbnail URL: {data['thumbnail_url']}\n")
                return data['thumbnail_url']
            else:
                print(f"⚠️ No thumbnail_url in response: {data}\n")
        else:
            print(f"❌ Failed with status {response.status_code}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    # Method 2: Instagram oEmbed
    print("Method 2: Instagram Direct oEmbed")
    try:
        oembed_endpoint = f"https://www.instagram.com/p/oembed/?url={clean_url}"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(oembed_endpoint, headers=headers, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            if 'thumbnail_url' in data:
                print(f"✅ SUCCESS! Thumbnail URL: {data['thumbnail_url']}\n")
                return data['thumbnail_url']
            else:
                print(f"⚠️ No thumbnail_url in response\n")
        else:
            print(f"❌ Failed with status {response.status_code}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    # Method 3: Scrape page
    print("Method 3: Scraping Instagram Page")
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
        response = requests.get(clean_url, headers=headers, timeout=15, allow_redirects=True)
        
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            patterns = [
                (r'"display_url":"(https://[^"]+)"', 'JSON display_url'),
                (r'<meta property="og:image" content="([^"]+)"', 'og:image meta tag'),
                (r'<meta name="twitter:image" content="([^"]+)"', 'twitter:image meta tag'),
            ]
            
            for pattern, name in patterns:
                match = re.search(pattern, response.text)
                if match:
                    thumbnail = match.group(1).replace('\\u0026', '&').replace('&amp;', '&')
                    print(f"✅ SUCCESS via {name}!")
                    print(f"Thumbnail URL: {thumbnail}\n")
                    return thumbnail
            
            print("⚠️ No thumbnail patterns found in HTML\n")
        else:
            print(f"❌ Failed with status {response.status_code}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
    
    print("❌ All methods failed - would use fallback image\n")
    return None

# Test with sample Instagram URLs
if __name__ == "__main__":
    # Example Instagram reel URL - replace with actual URL
    test_url = "https://www.instagram.com/reel/C_example/"
    
    print("=" * 60)
    print("Instagram Thumbnail Fetcher Test")
    print("=" * 60)
    print("\nREPLACE THE TEST URL WITH A REAL INSTAGRAM LINK!")
    print(f"Current test URL: {test_url}")
    print("\nTo test, edit line 81 with a real Instagram link and run:")
    print("python test_thumbnail.py")
    print("=" * 60)
    
    # Uncomment below and add real URL to test
    # result = test_instagram_thumbnail("https://www.instagram.com/reel/YOUR_REEL_ID/")
