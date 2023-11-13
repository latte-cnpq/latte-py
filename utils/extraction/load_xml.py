import os
from xml.etree import ElementTree as ET
from researcher.models import Researcher
from core.settings import BASE_DIR
from pathlib import Path

from .load_productions import get_books, get_books_chapters, get_published_articles
from .load_institutes import get_institutes

RESUME_PATH = Path(BASE_DIR, "resources", "xml").resolve()


def load_data_from_xml_folder():
    print(f"\n[Initiating XML extraction]\n")
    researchers = Researcher.objects.all()
    for filename in os.listdir(RESUME_PATH):
        if filename.endswith(".xml"):
            try:
                file_path = os.path.join(RESUME_PATH, filename)
                tree = ET.parse(file_path)
                root = tree.getroot()

                researcher_id = filename.split(".")[0]

                full_name = root.find(".//DADOS-GERAIS").get("NOME-COMPLETO")
                citation_names = root.find(".//DADOS-GERAIS").get(
                    "NOME-EM-CITACOES-BIBLIOGRAFICAS"
                )
                resume_text = root.find(".//RESUMO-CV").get("TEXTO-RESUMO-CV-RH")

                print(f"Processing file {filename} - Researcher ID: {researcher_id}")

                if not researchers.filter(researcher_id=researcher_id).exists():
                    researcher = Researcher.objects.create(
                        name=full_name,
                        resume=resume_text,
                        researcher_id=researcher_id,
                        citation_names=citation_names,
                    )
                    print(f"Researcher created: {researcher}")
                else:
                    researcher = researchers.filter(researcher_id=researcher_id).first()
                    print(
                        f"Researcher ID {researcher_id} already exists. Skipping creation."
                    )

                get_institutes(researcher, root)
                get_published_articles(researcher, root)
                get_books(researcher, root)
                get_books_chapters(researcher, root)

                print("\n")

            except Exception as e:
                print(f"Error processing file {filename}: {e}\n")

    print("[Finished XML extraction]\n")
