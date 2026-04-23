import requests
import time
from .models import URLCheck
from django.contrib.auth.models import User
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def monitor_all_urls():
    print("🔄 Running background monitoring...")

    users = User.objects.all()

    for user in users:
        urls = URLCheck.objects.filter(user=user).values_list('url', flat=True).distinct()

        for url in urls:

            if not url.startswith("http"):
                url = "https://" + url

            headers = {
                "User-Agent": "Mozilla/5.0",
                "Accept": "text/html"
            }

            MAX_RETRIES = 3
            DELAY = 2

            success = False
            response_time = None

            for attempt in range(MAX_RETRIES):
                try:
                    start_time = time.time()

                    response = requests.get(
                        url,
                        headers=headers,
                        timeout=8,
                        allow_redirects=True,
                        verify=False
                    )

                    response_time = round((time.time() - start_time) * 1000, 2)

                    # ✅ Only 200 is success
                    if response.status_code == 200:
                        success = True
                        break

                except:
                    pass

                time.sleep(DELAY)

            # Final result
            if success:
                status = "Active"
                health = "Good" if response_time and response_time < 1000 else "Slow"
            else:
                status = "Broken"
                health = "Failed after retries"

            # Save to DB
            URLCheck.objects.create(
                user=user,
                url=url,
                status=status,
                response_time=response_time,
                health=health
            )