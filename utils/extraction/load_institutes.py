from institutes.models import Institute
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
