from django.db import models
from django.contrib.auth.models import User

class URLCheck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()   # ✅ ADDED (VERY IMPORTANT)
    status = models.CharField(max_length=20)
    response_time = models.FloatField(null=True, blank=True)
    health = models.CharField(max_length=20)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.url
    
# 🚀 NEW MODEL (CLOUD REPORT STORAGE)
class CloudReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file_url = models.URLField()
    file_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    file_size = models.FloatField(default=0)  # in KB
    public_id=models.CharField(max_length=225,blank=True,null=True)

    def __str__(self):
        return self.file_name