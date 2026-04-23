from fileinput import filename
#import resource

from django.shortcuts import render, redirect
from .models import URLCheck, CloudReport   # ✅ UPDATED
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import csv
import sys
import json
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from django.shortcuts import get_object_or_404

# 🔥 CLOUD STORAGE IMPORTS
import cloudinary.uploader
from io import StringIO

# Only import if not on Windows
if sys.platform != 'win32':
    import resource
else:
    resource = None # Or mock the functionality if needed

def home(request):
    return render(request, "index.html")


@login_required
def dashboard(request):
    records = URLCheck.objects.filter(user=request.user)

    latest_records = {}
    for r in records.order_by('-checked_at'):
        if r.url not in latest_records:
            latest_records[r.url] = r

    unique_records = list(latest_records.values())

    total = len(unique_records)
    active = len([r for r in unique_records if r.status == "Active"])
    broken = len([r for r in unique_records if r.status == "Broken"])

    context = {
        "records": unique_records,
        "total": total,
        "active": active,
        "broken": broken
    }

    return render(request, "dashboard.html", context)


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        User.objects.create_user(username=username, password=password)
        return redirect("/login/")

    return render(request, "signup.html")


# =========================================
# ✅ LOCAL CSV DOWNLOAD
# =========================================
@login_required
def export_csv(request):
    records = URLCheck.objects.filter(user=request.user)

    now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"cloudmonitor_report_{now}.csv"

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(['URL', 'Status', 'Response Time', 'Health', 'Checked At'])

    for r in records:
        writer.writerow([r.url, r.status, r.response_time, r.health, r.checked_at])

    return response


# =========================================
# 🚀 CLOUD CSV EXPORT + SAVE TO DB
# =========================================
@login_required
@login_required
def export_csv_cloud(request):
    user = request.user
    records = URLCheck.objects.filter(user=user)

    buffer = StringIO()
    writer = csv.writer(buffer)

    writer.writerow(["URL", "Status", "Response Time", "Health", "Checked At"])

    for r in records:
        writer.writerow([
            r.url,
            r.status,
            r.response_time,
            r.health,
            r.checked_at
        ])

    # ✅ GET CSV DATA
    csv_data = buffer.getvalue()

    # ✅ CALCULATE SIZE
    file_size_kb = len(csv_data.encode()) / 1024

    filename = f"cloudmonitor_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

    try:
        # ✅ CORRECT (IMPORTANT: encode())
        upload_response = cloudinary.uploader.upload(
            csv_data.encode(),   # ✅ FIXED
            resource_type="raw",
            public_id=filename
        )

        file_url = upload_response["secure_url"]
        public_id = upload_response["public_id"]

        from .models import CloudReport

        CloudReport.objects.create(
            user=user,
            file_name=filename + ".csv",
            file_url=file_url,
            file_size=file_size_kb,
            public_id=public_id
        )

        return JsonResponse({
            "status": "success",
            "message": "Uploaded successfully",
            "file_url": file_url
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        })

# =========================================
# JSON DOWNLOAD
# =========================================
@login_required
def export_json(request):
    records = URLCheck.objects.filter(user=request.user)

    data = list(records.values())

    now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"cloudmonitor_report_{now}.json"

    response = JsonResponse(data, safe=False)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response


# =========================================
# 📁 NEW PAGE → MY REPORTS
# =========================================
@login_required
def reports_page(request):
    from .models import CloudReport

    reports = CloudReport.objects.filter(user=request.user)

    # ✅ TOTAL STORAGE
    total_storage = sum(r.file_size for r in reports)

    total_files = reports.count()

    # ✅ SET LIMIT (5MB FREE DEMO)
    MAX_STORAGE = 5000  # in KB

    usage_percent = (total_storage / MAX_STORAGE) * 100 if MAX_STORAGE else 0

    return render(request, "reports.html", {
        "reports": reports,
        "total_storage": total_storage,
        "total_files": total_files,
        "usage_percent": usage_percent,
        "max_storage": MAX_STORAGE
    })
# =========================================
# 📡 MONITOR PAGE
# =========================================
@login_required
def monitor_page(request):
    urls = URLCheck.objects.filter(user=request.user)\
        .values_list('url', flat=True).distinct()

    stats = {}

    for url in urls:
        data = URLCheck.objects.filter(user=request.user, url=url)

        total = data.count()
        active = data.filter(status="Active").count()
        broken = data.filter(status="Broken").count()

        uptime = round((active / total) * 100, 2) if total > 0 else 0

        stats[url] = {
            "total": total,
            "active": active,
            "broken": broken,
            "uptime": uptime
        }

    return render(request, "monitor.html", {
        "urls": urls,
        "stats": stats
    })


# =========================================
# 📊 GRAPH DATA API
# =========================================
@login_required
def get_url_data(request):
    url = request.GET.get("url")

    data = URLCheck.objects.filter(user=request.user, url=url)\
        .order_by('checked_at')

    response = [
        {
            "time": str(d.checked_at),
            "response_time": d.response_time
        }
        for d in data
    ]

    return JsonResponse(response, safe=False)



@login_required
def view_report(request, report_id):
    report = CloudReport.objects.get(id=report_id, user=request.user)

    import requests
    response = requests.get(report.file_url)

    content = response.content.decode("utf-8").splitlines()

    import csv
    reader = csv.reader(content)

    data = list(reader)

    headers = data[0]
    rows = data[1:]

    return render(request, "view_report.html", {
        "report": report,
        "headers": headers,
        "rows": rows
    })

@login_required
def delete_report(request, report_id):
    from .models import CloudReport

    report=CloudReport.objects.get(id=report_id,user=request.user)
    if request.method=="POST":
        #DELETE from cloudinary
        if report.public_id:
            try:
                cloudinary.uploader.destroy(report.public_id,resource_type="raw")
            except Exception as e:
                print("Cloud delete error:",e)
        
        # Delete from DB
        report.delete()

    return redirect("/reports/")