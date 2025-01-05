from django.core.management.base import BaseCommand
from sales.views import GenerateReport
from django_crontab.crontab import Crontab

class Command(BaseCommand):
    help = 'Generate daily report'

    def handle(self, *args, **kwargs):
        # Call the report generation view
        report_view = GenerateReport.as_view()
        request = None  # Create a request object as needed for the view
        response = report_view(request)
        with open('daily_report.pdf', 'wb') as f:
            f.write(response.content)
