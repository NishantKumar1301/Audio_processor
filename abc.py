import os
import django
import glob
from django.db import connection

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")  # Replace `your_project` with your actual Django project name
django.setup()

def drop_django_celery_beat_tables():
    """Drops all tables related to django_celery_beat, including system tables."""
    with connection.cursor() as cursor:
        cursor.execute("""
            DO $$ 
            DECLARE 
                r RECORD;
            BEGIN 
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename LIKE 'django_celery_beat%') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """)
    print("✅ All `django_celery_beat` tables removed successfully!")

def delete_migration_files():
    """Deletes all django_celery_beat migration files except __init__.py."""
    migrations_path = "django_celery_beat/migrations/"

    # Find all migration files except __init__.py
    migration_files = glob.glob(os.path.join(migrations_path, "*.py"))
    migration_files = [f for f in migration_files if not f.endswith("__init__.py")]

    # Delete each migration file
    for file in migration_files:
        os.remove(file)
        print(f"✅ Deleted: {file}")

    print("✅ All old migration files removed!")

if __name__ == "__main__":
    print("🔄 Starting cleanup process...")
    drop_django_celery_beat_tables()
    delete_migration_files()
    print("🎉 Cleanup completed successfully!")
 # type: ignore