import os
import django
from django.db import connection

# Initialize Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")  # Replace 'project' with your actual project name
django.setup()

def reset_django_celery_beat():
    with connection.cursor() as cursor:
        tables = [
            "django_celery_beat_clockedschedule",
            "django_celery_beat_crontabschedule",
            "django_celery_beat_intervalschedule",
            "django_celery_beat_periodictask",
            "django_celery_beat_solarschedule",
            "django_celery_beat_periodictasks",
        ]

        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
            print(f"✅ Deleted table {table}")

        print("✅ All `django_celery_beat` tables removed successfully!")

if __name__ == "__main__":
    print("🔄 Starting cleanup process...")
    reset_django_celery_beat()
    print("🎉 Cleanup completed successfully!")
 # type: ignore