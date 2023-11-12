import os
from xml.etree import ElementTree as ET
from researcher.models import Researcher
from core.settings import BASE_DIR
from pathlib import Path
from institutes.models import Institute
from productions.models import Article, PublishedBook, PublishedChapter
from django.db import transaction

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
                resume_text = root.find(".//RESUMO-CV").get("TEXTO-RESUMO-CV-RH")

                print(f"Processing file {filename} - Researcher ID: {researcher_id}")

                if not researchers.filter(researcher_id=researcher_id).exists():
                    researcher = Researcher.objects.create(
                        name=full_name,
                        resume=resume_text,
                        researcher_id=researcher_id,
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


def get_published_articles(researcher, root):
    print(f"Trying to get {researcher}'s articles...")

    all_articles = Article.objects.all().filter(researcher=researcher)
    productions = root.find(".//PRODUCAO-BIBLIOGRAFICA")

    if productions is not None:
        articles = productions.find(".//ARTIGOS-PUBLICADOS")

        if articles is not None:
            article_count = 0

            for pub_article in articles:
                article_basic_data = pub_article.find(".//DADOS-BASICOS-DO-ARTIGO")

                if article_basic_data is not None:
                    title = article_basic_data.get("TITULO-DO-ARTIGO")
                    nature = article_basic_data.get("NATUREZA")
                    year = article_basic_data.get("ANO-DO-ARTIGO")
                    language = article_basic_data.get("IDIOMA")

                    article_details = pub_article.find(".//DETALHAMENTO-DO-ARTIGO")

                    if article_details is not None:
                        periodical_title = article_details.get(
                            "TITULO-DO-PERIODICO-OU-REVISTA"
                        )
                        volume = article_details.get("VOLUME")
                        pages = article_details.get("PAGINA-FINAL")
                        publication_location = article_details.get(
                            "LOCAL-DE-PUBLICACAO"
                        )

                        homepage = article_basic_data.get("HOME-PAGE-DO-TRABALHO")
                        dissemination_medium = article_basic_data.get(
                            "MEIO-DE-DIVULGACAO"
                        )

                        if not all_articles.filter(title=title).exists():
                            Article.objects.create(
                                title=title,
                                nature=nature,
                                year=year,
                                language=language,
                                periodical_title=periodical_title,
                                volume=volume,
                                pages=pages,
                                publication_location=publication_location,
                                homepage=homepage,
                                dissemination_medium=dissemination_medium,
                                researcher=researcher,
                            )

                            article_count += 1

            print(f"Found {article_count} new articles for {researcher}.")
        else:
            print(f"No ARTIGOS-PUBLICADOS found for {researcher}.")
    else:
        print(f"No PRODUCAO-BIBLIOGRAFICA found for {researcher}.")


def get_books_chapters(researcher, root):
    print(f"Trying to get {researcher}'s book chapters...")

    all_chapters = PublishedChapter.objects.all().filter(researcher=researcher)
    productions = root.find(".//PRODUCAO-BIBLIOGRAFICA")

    if productions is not None:
        books_and_chapters = productions.find(".//LIVROS-E-CAPITULOS")

        if books_and_chapters is not None:
            chapters = books_and_chapters.find(".//CAPITULOS-DE-LIVROS-PUBLICADOS")

            if chapters is not None:
                chapters_count = 0

                for chapter in chapters:
                    chapter_basic_data = chapter.find(".//DADOS-BASICOS-DO-CAPITULO")

                    if chapter_basic_data is not None:
                        title = chapter_basic_data.get("TITULO-DO-CAPITULO-DO-LIVRO")
                        nature = chapter_basic_data.get("TIPO")
                        year = chapter_basic_data.get("ANO")
                        language = chapter_basic_data.get("IDIOMA")
                        dissemination_medium = chapter_basic_data.get(
                            "MEIO-DE-DIVULGACAO"
                        )

                        chapter_details = chapter.find(".//DETALHAMENTO-DO-CAPITULO")

                        if chapter_details is not None:
                            book_title = chapter_details.get("TITULO-DO-LIVRO")
                            organizers = chapter_details.get("ORGANIZADORES")
                            pages = chapter_details.get("PAGINA-FINAL")
                            publisher = chapter_details.get("NOME-DA-EDITORA")

                            if not all_chapters.filter(title=title).exists():
                                PublishedChapter.objects.create(
                                    title=title,
                                    nature=nature,
                                    year=year,
                                    language=language,
                                    dissemination_medium=dissemination_medium,
                                    book_title=book_title,
                                    organizers=organizers,
                                    pages=pages,
                                    publisher=publisher,
                                    researcher=researcher,
                                )

                                chapters_count += 1

                print(f"Found {chapters_count} new book chapters for {researcher}.")
            else:
                print(f"No CAPITULOS-DE-LIVROS-PUBLICADOS found for {researcher}.")
        else:
            print(f"No LIVROS-E-CAPITULOS found for {researcher}")
    else:
        print(f"No PRODUCAO-BIBLIOGRAFICA found for {researcher}.")


def get_books(researcher, root):
    print(f"Trying to get {researcher}'s books...")

    all_books = PublishedBook.objects.all().filter(researcher=researcher)
    productions = root.find(".//PRODUCAO-BIBLIOGRAFICA")

    if productions is not None:
        books_and_chapters = productions.find(".//LIVROS-E-CAPITULOS")

        if books_and_chapters is not None:
            books = books_and_chapters.find(".//LIVROS-PUBLICADOS-OU-ORGANIZADOS")

            if books is not None:
                books_count = 0

                for chapter in books:
                    chapter_basic_data = chapter.find(".//DADOS-BASICOS-DO-LIVRO")

                    if chapter_basic_data is not None:
                        title = chapter_basic_data.get("TITULO-DO-LIVRO")
                        nature = chapter_basic_data.get("TIPO")
                        year = chapter_basic_data.get("ANO")
                        language = chapter_basic_data.get("IDIOMA")
                        dissemination_medium = chapter_basic_data.get(
                            "MEIO-DE-DIVULGACAO"
                        )

                        chapter_details = chapter.find(".//DETALHAMENTO-DO-LIVRO")

                        if chapter_details is not None:
                            volume = chapter_details.get("NUMERO-DE-VOLUMES")
                            pages = chapter_details.get("NUMERO-DE-PAGINAS")
                            publisher = chapter_details.get("NOME-DA-EDITORA")

                            if not all_books.filter(title=title).exists():
                                PublishedBook.objects.create(
                                    title=title,
                                    nature=nature,
                                    year=year,
                                    language=language,
                                    dissemination_medium=dissemination_medium,
                                    volume=volume,
                                    pages=pages,
                                    publisher=publisher,
                                    researcher=researcher,
                                )

                                books_count += 1

                print(f"Found {books_count} new books for {researcher}.")
            else:
                print(f"No LIVROS-PUBLICADOS-OU-ORGANIZADOS found for {researcher}.")
        else:
            print(f"No LIVROS-E-CAPITULOS found for {researcher}")
    else:
        print(f"No PRODUCAO-BIBLIOGRAFICA found for {researcher}.")


from django.db import transaction


from django.db import transaction


def get_institutes(researcher, root):
    print(f"Trying to get {researcher}'s institutes...")

    # Encontrar dados complementares
    additional_data = root.find(".//DADOS-COMPLEMENTARES")

    if additional_data is not None:
        # Encontrar informações adicionais sobre instituições
        additional_institutes_data = additional_data.find(
            ".//INFORMACOES-ADICIONAIS-INSTITUICOES"
        )

        if additional_institutes_data is not None:
            institutes_to_add = []

            for institute_data in additional_institutes_data:
                # Verifica se os dados necessários estão presentes
                acronym = institute_data.get("SIGLA-INSTITUICAO")
                institute_code = institute_data.get("CODIGO-INSTITUICAO")
                country_acronym = institute_data.get("SIGLA-PAIS-INSTITUICAO")
                country = institute_data.get("NOME-PAIS-INSTITUICAO")

                if acronym:
                    # Verificar se a instituição com o mesmo código já existe
                    existing_institute = Institute.objects.filter(
                        acronym=acronym
                    ).first()

                    if not existing_institute:
                        # Criar a instituição se não existir
                        created_institute = Institute.objects.create(
                            acronym=acronym,
                            institute_code=institute_code,
                            country_acronym=country_acronym,
                            country=country,
                        )
                        institutes_to_add.append(created_institute)
                    else:
                        # Adicionar a instituição existente à lista para associar ao pesquisador
                        institutes_to_add.append(existing_institute)

            # Adicionar instituições ao campo ManyToManyField do pesquisador
            with transaction.atomic():
                researcher.institutes.add(*institutes_to_add)

            print(f"Added {len(institutes_to_add)} institutes to {researcher}.")
        else:
            print("No INFORMACOES-ADICIONAIS-INSTITUICOES found.")
    else:
        print("No DADOS-COMPLEMENTARES found.")
