from django.core.management.base import BaseCommand, CommandError
from utils.carga import load_data_from_xml_folder


class Command(BaseCommand):
    help = "Realiza carga dos dados dos xmls"

    def handle(self, *args, **options):
        load_data_from_xml_folder()
        self.stdout.write(self.style.SUCCESS("Successfully closed poll"))
