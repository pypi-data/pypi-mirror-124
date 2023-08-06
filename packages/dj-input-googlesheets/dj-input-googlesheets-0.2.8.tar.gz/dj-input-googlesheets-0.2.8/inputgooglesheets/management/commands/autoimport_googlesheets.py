from django.core.management.base import BaseCommand
from ...spreadsheetservice import SpreadSheetService
from ...importservice import ImportService


class Command(BaseCommand):
    help = 'Periodically import autoimportable google spreadsheets.'

    def handle(self, *args, **options):
        import_service = ImportService(SpreadSheetService)
        import_service.autoimport_forever()
