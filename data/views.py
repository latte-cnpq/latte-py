from rest_framework import viewsets, status
from researcher.models import Researcher
from productions.models import Production
from rest_framework.response import Response
import igraph as ig
from igraph import plot
from core.settings import MEDIA_ROOT, MEDIA_URL
import os


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
                    graph.add_edge(
                        researcher_ids[production.researcher.id],
                        researcher_ids[collaborator.id],
                        type="collaboration",
                    )

        # Get color range values from query parameters with fallback values
        red_end = int(request.query_params.get("red_end", 10))
        yellow_end = int(request.query_params.get("yellow_end", 20))

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
        vertex_sizes = [30 + 5 * len(graph.incident(v, mode=ig.IN)) for v in graph.vs]
        vertex_labels = [
            f"{v['name']} \n ({len(graph.incident(v, mode=ig.IN))} colaborações)"
            for v in graph.vs
        ]

        plot(
            graph,
            layout=layout,
            target=media_path,
            vertex_label=vertex_labels,
            vertex_size=vertex_sizes,
            vertex_color=graph.vs["color"],
            edge_width=2,
            edge_color="#EDEEF0",
            vertex_label_size=16,
            bbox=(1920, 1080),
            margin=150,
            vertex_label_dist=2,
            background="#18191B",
            vertex_label_color="white",
        )

        media_url = request.build_absolute_uri(MEDIA_URL + "collaboration_graph.png")

        return Response(
            {
                "message": "Collaboration graph created and saved as collaboration_graph.png",
                "media_url": media_url,
            },
            status=status.HTTP_201_CREATED,
        )
