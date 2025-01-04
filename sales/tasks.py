from celery import shared_task
from django.utils import timezone
from .models import ClientRecord
import os
from django.core.files.storage import default_storage

@shared_task
def generate_daily_report():
    # Fetch the client records
    client_records = ClientRecord.objects.all()

    # Prepare the report
    report_file = f"daily_report_{timezone.now().strftime('%Y-%m-%d')}.csv"
    report_path = os.path.join('/path/to/reports', report_file)


    with open(report_path, 'w') as file:
        file.write("ID, Name, Contact\n")
        for record in client_records:
            file.write(f"{record.id}, {record.name}, {record.contact_info}\n")


    # Save to a secure backup (e.g., AWS S3 or Azure Blob Storage)
    backup_file = default_storage.save(f"backups/{report_file}", report_path)
    return f"Backup saved as {backup_file}"