from django.core.management.base import BaseCommand, CommandError
from utils.extraction.load_xml import load_data_from_xml_folder


class Command(BaseCommand):
    help = "Realiza carga dos dados dos xmls"

    def handle(self, *args, **options):
        load_data_from_xml_folder()
        self.stdout.write(self.style.SUCCESS("Successfully extracted data from XML"))
