from django.apps import AppConfig
import sys
import atexit


class CheckerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checker'

    def ready(self):
        # 🚫 Prevent running during migrations, shell, etc.
        if not (len(sys.argv) > 1 and sys.argv[1] == 'runserver'):
            return

        # 🚫 Prevent double execution (Django reload issue)
        if hasattr(self, 'scheduler_started') and self.scheduler_started:
            return

        from apscheduler.schedulers.background import BackgroundScheduler
        from .tasks import monitor_all_urls

        scheduler = BackgroundScheduler()

        # 🔥 Background monitoring job (with retry system already inside tasks.py)
        scheduler.add_job(
            monitor_all_urls,
            'interval',
            seconds=30,
            id='monitor_job',
            replace_existing=True,
            max_instances=1,   # already default but explicit
            coalesce=True      # skip overlapping jobs
        )

        scheduler.start()

        print("✅ Background Scheduler Started...")

        # Mark as started (prevents duplicate)
        self.scheduler_started = True

        # Graceful shutdown
        atexit.register(lambda: scheduler.shutdown())