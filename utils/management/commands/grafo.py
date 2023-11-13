from django.core.management.base import BaseCommand
import igraph as ig
from igraph import plot
from researcher.models import Researcher
from productions.models import Production
import matplotlib.pyplot as plt


class Command(BaseCommand):
    help = "Creates a collaboration graph based on Django models using igraph and saves it as an image"

    def handle(self, *args, **options):
        # Create an empty graph
        graph = ig.Graph()

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

        # Create a plot and save it as an image
        layout = graph.layout("kk")  # You can use a different layout algorithm
        plot(
            graph,
            layout=layout,
            target="collaboration_graph.png",
            vertex_label=graph.vs["name"],
            vertex_size=20,
            edge_width=1,
            vertex_label_size=10,
            bbox=(1200, 800),
            margin=100,
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Collaboration graph created and saved as collaboration_graph.png"
            )
        )
