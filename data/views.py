from rest_framework import viewsets, status
from researcher.models import Researcher
from productions.models import Production
from institutes.models import Institute
from rest_framework.response import Response
import igraph as ig
from igraph import plot
from core.settings import MEDIA_ROOT, MEDIA_URL
import os
from django.core.exceptions import ValidationError


class CollaborationGraphViewSet(viewsets.ViewSet):
    def list(self, request):
        graph = ig.Graph()

        media_path = os.path.join(MEDIA_ROOT, "collaboration_graph.png")

        # Create media directory if it doesn't exist
        media_dir = os.path.dirname(media_path)
        os.makedirs(media_dir, exist_ok=True)

        # Add vertices for researchers
        researchers = Researcher.objects.all()
        researcher_ids = {
            researcher.id: graph.add_vertex(name=researcher.name, type="researcher")
            for researcher in researchers
        }

        productions = Production.objects.all()

        # Add edges based on collaborations between researchers
        for production in productions:
            collaborators = production.authors.all()
            # Add edge only if there are more than one collaborator
            if collaborators.count() >= 1:
                for collaborator in collaborators:
                    edge = graph.add_edge(
                        researcher_ids[production.researcher.id],
                        researcher_ids[collaborator.id],
                        type="collaboration",
                    )

        # Get color range values from query parameters with fallback values
        red_end = int(request.query_params.get("red_end", 1))
        yellow_end = int(request.query_params.get("yellow_end", 4))

        # Get color intervals with fallback values
        color_intervals = {
            (0, red_end): "red",
            (red_end + 1, yellow_end): "yellow",
            (yellow_end + 1, float("inf")): "green",
        }

        # Set vertex color based on the number of edges and color intervals
        for v in graph.vs:
            num_edges = len(graph.incident(v, mode=ig.IN))
            color = "gray"  # Default color

            for interval, interval_color in color_intervals.items():
                if interval[0] <= num_edges <= interval[1]:
                    color = interval_color
                    break

            v["color"] = color

        # Create a plot and save it as an image
        layout = graph.layout("kk")  # You can use a different layout algorithm
        graph.simplify(combine_edges={"type": "first"})

        vertex_sizes = [30 + 5 * len(graph.incident(v, mode=ig.IN)) for v in graph.vs]
        vertex_labels = [f"{v['name']}" for v in graph.vs]

        plot(
            graph,
            layout=layout,
            target=media_path,
            vertex_label=vertex_labels,
            vertex_label_size=16,
            vertex_label_dist=2,
            vertex_label_color="white",
            vertex_size=vertex_sizes,
            vertex_color="#8E4EC6",
            edge_width=2,
            edge_color=graph.vs["color"],
            edge_label_color="white",
            bbox=(1920, 1080),
            margin=150,
            background="#18191B",
        )

        media_url = request.build_absolute_uri(MEDIA_URL + "collaboration_graph.png")

        return Response(
            {
                "message": "Collaboration graph created and saved as collaboration_graph.png",
                "media_url": media_url,
            },
            status=status.HTTP_201_CREATED,
        )


from django.db.models import Count
from django.db.models import Q


class ColumnDataViewSet(viewsets.ViewSet):
    def list(self, request):
        start_year = request.query_params.get("startYear", None)
        end_year = request.query_params.get("endYear", None)
        researcher = request.query_params.get("researcherName", None)
        institute = request.query_params.get("instituteName", None)
        type = request.query_params.get("type", None)

        # Filtra o queryset com base nos parâmetros fornecidos
        queryset = Production.objects.all()
        if researcher:
            queryset = queryset.filter(researcher__name__icontains=researcher)
        if institute:
            queryset = queryset.filter(
                researcher__institutes__acronym__icontains=institute
            )
        if start_year and end_year:
            try:
                start_year = int(start_year)
                end_year = int(end_year)
                queryset = queryset.filter(year__range=(start_year, end_year))
            except ValueError:
                raise ValidationError("Invalid start_year or end_year format.")
        elif start_year:
            try:
                start_year = int(start_year)
                queryset = queryset.filter(year__gte=start_year)
            except ValueError:
                raise ValidationError("Invalid start_year format.")
        elif end_year:
            try:
                end_year = int(end_year)
                queryset = queryset.filter(year__lte=end_year)
            except ValueError:
                raise ValidationError("Invalid end_year format.")
        if type:
            queryset = queryset.filter(type=type)

        # Agrupa por ano e conta o número de artigos e livros
        result = (
            queryset.values("year")
            .annotate(
                totalArticles=Count("pk", filter=Q(type=1)),
                totalBooks=Count("pk", filter=Q(type=2)),
                totalChapters=Count("pk", filter=Q(type=3)),
            )
            .order_by("year")
        )

        # Formata o resultado como uma lista de dicionários
        formatted_result = [
            {
                "year": str(item["year"]),
                "totalArticles": item["totalArticles"],
                "totalBooks": item["totalBooks"],
                "totalChapters": item["totalChapters"],
            }
            for item in result
        ]

        return Response({"results": formatted_result})


class TotalProductionsViewSet(viewsets.ViewSet):
    def list(self, request):
        start_year = request.query_params.get("startYear", None)
        end_year = request.query_params.get("endYear", None)
        researcher = request.query_params.get("researcherName", None)
        institute = request.query_params.get("instituteName", None)
        type = request.query_params.get("type", None)

        # Filtra o queryset com base nos parâmetros fornecidos
        queryset = Production.objects.all()
        if researcher:
            queryset = queryset.filter(researcher__name__icontains=researcher)
        if institute:
            queryset = queryset.filter(
                researcher__institutes__acronym__icontains=institute
            )
        if start_year and end_year:
            try:
                start_year = int(start_year)
                end_year = int(end_year)
                queryset = queryset.filter(year__range=(start_year, end_year))
            except ValueError:
                raise ValidationError("Invalid start_year or end_year format.")
        elif start_year:
            try:
                start_year = int(start_year)
                queryset = queryset.filter(year__gte=start_year)
            except ValueError:
                raise ValidationError("Invalid start_year format.")
        elif end_year:
            try:
                end_year = int(end_year)
                queryset = queryset.filter(year__lte=end_year)
            except ValueError:
                raise ValidationError("Invalid end_year format.")
        if type:
            queryset = queryset.filter(type=type)

        # Conta o número total de artigos, livros e capítulos
        total_productions = queryset.count()
        total_articles = queryset.filter(type=1).count()
        total_books = queryset.filter(type=2).count()
        total_chapters = queryset.filter(type=3).count()

        # Retorna a resposta formatada
        response_data = {
            "totalProductions": total_productions,
            "totalArticles": total_articles,
            "totalBooks": total_books,
            "totalChapters": total_chapters,
        }

        return Response(response_data)


class TotalResearchersInstitutesViewSet(viewsets.ViewSet):
    def list(self, request):
        start_year = request.query_params.get("startYear", None)
        end_year = request.query_params.get("endYear", None)
        researcher = request.query_params.get("researcherName", None)
        institute = request.query_params.get("instituteName", None)
        type = request.query_params.get("type", None)

        # Filtra o queryset com base nos parâmetros fornecidos
        researcher_queryset = Researcher.objects.all()
        institute_queryset = Institute.objects.all()

        if researcher:
            researcher_queryset = researcher_queryset.filter(name__icontains=researcher)
        if institute:
            institute_queryset = institute_queryset.filter(acronym__icontains=institute)

        # Conta o número total de pesquisadores e institutos
        total_researchers = researcher_queryset.count()
        total_institutes = institute_queryset.count()

        # Retorna a resposta formatada
        response_data = {
            "totalResearchers": total_researchers,
            "totalInstitutes": total_institutes,
        }

        return Response(response_data)
