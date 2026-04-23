'''from ninja import NinjaAPI
import requests
from concurrent.futures import ThreadPoolExecutor
import time
from .models import URLCheck

api = NinjaAPI()

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_single_url(data):
    url, user = data

    if not url.startswith("http"):
        url = "https://" + url

    url = url.strip()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/xhtml+xml"
    }

    try:
        start_time = time.time()

        response = requests.get(
            url,
            headers=headers,
            timeout=10,
            allow_redirects=True,
            verify=False
        )

        response_time = round((time.time() - start_time) * 1000, 2)

        if 200 <= response.status_code < 400:
            status = "Active"
            health = "Good" if response_time < 500 else "Slow"
        else:
            status = "Broken"
            health = "Poor"

    except requests.exceptions.Timeout:
        status = "Broken"
        response_time = None
        health = "Timeout"

    except requests.exceptions.ConnectionError:
        status = "Broken"
        response_time = None
        health = "Connection Error"

    except Exception:
        status = "Broken"
        response_time = None
        health = "Error"

    if user.is_authenticated:
        URLCheck.objects.create(
            user=user,
            url=url,
            status=status,
            response_time=response_time,
            health=health
        )

    return {
        "url": url,
        "status": status,
        "response_time": response_time,
        "health": health
    }


@api.post("/check")
def check_links(request, urls: list[str]):
    data = [(url, request.user) for url in urls]

    # Run in parallel (faster checking)
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(check_single_url, data))

    return results'''



from ninja import NinjaAPI
import requests
from concurrent.futures import ThreadPoolExecutor
import time
from .models import URLCheck

# Disable SSL warnings (because of verify=False)
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

api = NinjaAPI()


def check_single_url(data):
    url, user = data

    # Ensure proper format
    if not url.startswith("http"):
        url = "https://" + url

    url = url.strip()

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Accept": "text/html,application/xhtml+xml"
    }

    try:
        start_time = time.time()

        response = requests.get(
            url,
            headers=headers,
            timeout=10,
            allow_redirects=True,
            verify=False
        )

        response_time = round((time.time() - start_time) * 1000, 2)

        # ✅ STRICT CHECK (FIXED)
        if response.status_code == 200:
            status = "Active"
            health = "Good" if response_time < 1000 else "Slow"
        else:
            status = "Broken"
            health = "Poor"

    except requests.exceptions.Timeout:
        status = "Broken"
        response_time = None
        health = "Timeout"

    except requests.exceptions.ConnectionError:
        status = "Broken"
        response_time = None
        health = "Connection Error"

    except requests.exceptions.InvalidURL:
        status = "Broken"
        response_time = None
        health = "Invalid URL"

    except Exception:
        status = "Broken"
        response_time = None
        health = "Error"

    # Save to DB
    if user.is_authenticated:
        URLCheck.objects.create(
            user=user,
            url=url,
            status=status,
            response_time=response_time,
            health=health
        )

    return {
        "url": url,
        "status": status,
        "response_time": response_time,
        "health": health
    }


@api.post("/check")
def check_links(request, urls: list[str]):
    data = [(url, request.user) for url in urls]

    # Run in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(check_single_url, data))

    return results