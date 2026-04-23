import time
import requests
from django.core.mail import send_mail
from .models import URLCheck
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings


def check_urls():
    while True:
        print("🔄 Running auto monitoring...")

        users = User.objects.all()

        for user in users:

            # 🚫 Skip if user has no email
            if not user.email:
                continue

            urls = URLCheck.objects.filter(user=user)\
                .values_list('url', flat=True).distinct()

            for url in urls:

                if not url.startswith("http"):
                    url = "https://" + url

                # 👉 Get last status
                last_record = URLCheck.objects.filter(user=user, url=url)\
                    .order_by('-checked_at').first()

                last_status = last_record.status if last_record else None

                try:
                    start = time.time()
                    response = requests.get(url, timeout=5)
                    response_time = round((time.time() - start) * 1000, 2)

                    if response.status_code == 200:
                        status = "Active"
                        health = "Good" if response_time < 500 else "Slow"
                    else:
                        status = "Broken"
                        health = "Poor"

                except Exception:
                    status = "Broken"
                    response_time = None
                    health = "Poor"

                # 🚨 DOWN ALERT
                if last_status != "Broken" and status == "Broken":
                    send_mail(
                        subject=f"🚨 ALERT: Website Down - {url}",
                        message=f"""
Hello {user.username},

⚠️ Your monitored website is DOWN.

🔗 URL: {url}
📉 Status: Broken
⏱ Time: {now().strftime('%Y-%m-%d %H:%M:%S')}

Please check your website immediately.

— Cloud Monitor 🚀
                        """,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email],
                        fail_silently=True,
                    )

                # ✅ RECOVERY ALERT
                if last_status == "Broken" and status == "Active":
                    send_mail(
                        subject=f"✅ RECOVERED: Website Back Online - {url}",
                        message=f"""
Hello {user.username},

🎉 Good news! Your website is back online.

🔗 URL: {url}
📈 Status: Active
⚡ Response Time: {response_time} ms
⏱ Time: {now().strftime('%Y-%m-%d %H:%M:%S')}

Everything is working normally now.

— Cloud Monitor 🚀
                        """,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[user.email],
                        fail_silently=True,
                    )

                # 💾 Save record
                URLCheck.objects.create(
                    user=user,
                    url=url,
                    status=status,
                    response_time=response_time,
                    health=health
                )

        time.sleep(10)