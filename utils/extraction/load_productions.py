from researcher.models import Researcher
from productions.models import Production, Article, PublishedBook, PublishedChapter


def process_autores(production, autores):
    autores_list = []

    for autor in autores:
        nome_completo = autor.get("NOME-COMPLETO-DO-AUTOR")

        # Verificar se o autor já existe no banco de dados
        researcher = Researcher.objects.filter(name=nome_completo).first()

        # Verificar se o pesquisador não é o mesmo que o autor do production
        if researcher and researcher.id and researcher.id != production.researcher.id:
            production.authors.add(researcher)

    production.save()


def get_published_articles(researcher, root):
    print(f"Trying to get {researcher}'s articles...")

    all_productions = Production.objects.all().filter(researcher=researcher)
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

                        if not all_productions.filter(title=title).exists():
                            production = Production.objects.create(
                                researcher=researcher,
                                title=title,
                                nature=nature,
                                year=year,
                                language=language,
                                dissemination_medium=dissemination_medium,
                                type="article",
                            )

                            autores = pub_article.findall("AUTORES")
                            process_autores(production, autores)

                            Article.objects.create(
                                production=production,
                                periodical_title=periodical_title,
                                volume=volume,
                                pages=pages,
                                publication_location=publication_location,
                                homepage=homepage,
                            )

                            article_count += 1

            print(f"Found {article_count} new articles for {researcher}.")
        else:
            print(f"No ARTIGOS-PUBLICADOS found for {researcher}.")
    else:
        print(f"No PRODUCAO-BIBLIOGRAFICA found for {researcher}.")


def get_books_chapters(researcher, root):
    print(f"Trying to get {researcher}'s book chapters...")

    all_productions = Production.objects.all().filter(researcher=researcher)
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

                            if not all_productions.filter(title=title).exists():
                                production = Production.objects.create(
                                    researcher=researcher,
                                    title=title,
                                    nature=nature,
                                    year=year,
                                    language=language,
                                    dissemination_medium=dissemination_medium,
                                    type="chapter",
                                )

                                autores = chapter.findall("AUTORES")
                                process_autores(production, autores)

                                PublishedChapter.objects.create(
                                    production=production,
                                    book_title=book_title,
                                    organizers=organizers,
                                    pages=pages,
                                    publisher=publisher,
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

    all_prodcutions = Production.objects.all().filter(researcher=researcher)
    productions = root.find(".//PRODUCAO-BIBLIOGRAFICA")

    if productions is not None:
        books_and_chapters = productions.find(".//LIVROS-E-CAPITULOS")

        if books_and_chapters is not None:
            books = books_and_chapters.find(".//LIVROS-PUBLICADOS-OU-ORGANIZADOS")

            if books is not None:
                books_count = 0

                for book in books:
                    chapter_basic_data = book.find(".//DADOS-BASICOS-DO-LIVRO")

                    if chapter_basic_data is not None:
                        title = chapter_basic_data.get("TITULO-DO-LIVRO")
                        nature = chapter_basic_data.get("TIPO")
                        year = chapter_basic_data.get("ANO")
                        language = chapter_basic_data.get("IDIOMA")
                        dissemination_medium = chapter_basic_data.get(
                            "MEIO-DE-DIVULGACAO"
                        )

                        chapter_details = book.find(".//DETALHAMENTO-DO-LIVRO")

                        if chapter_details is not None:
                            volume = chapter_details.get("NUMERO-DE-VOLUMES")
                            pages = chapter_details.get("NUMERO-DE-PAGINAS")
                            publisher = chapter_details.get("NOME-DA-EDITORA")

                            if not all_prodcutions.filter(title=title).exists():
                                production = Production.objects.create(
                                    researcher=researcher,
                                    title=title,
                                    nature=nature,
                                    year=year,
                                    language=language,
                                    dissemination_medium=dissemination_medium,
                                    type="book",
                                )

                                autores = book.findall("AUTORES")
                                process_autores(production, autores)

                                PublishedBook.objects.create(
                                    production=production,
                                    volume=volume,
                                    pages=pages,
                                    publisher=publisher,
                                )

                                books_count += 1

                print(f"Found {books_count} new books for {researcher}.")
            else:
                print(f"No LIVROS-PUBLICADOS-OU-ORGANIZADOS found for {researcher}.")
        else:
            print(f"No LIVROS-E-CAPITULOS found for {researcher}")
    else:
        print(f"No PRODUCAO-BIBLIOGRAFICA found for {researcher}.")
