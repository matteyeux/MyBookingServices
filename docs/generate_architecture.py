from diagrams import Cluster
from diagrams import Diagram
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.elastic.elasticsearch import Kibana
from diagrams.elastic.elasticsearch import Logstash
from diagrams.generic.network import VPN
from diagrams.onprem.client import Client
from diagrams.onprem.container import Docker
from diagrams.onprem.database import Mysql
from diagrams.onprem.network import Traefik
from diagrams.onprem.vcs import Gitlab
from diagrams.programming.framework import Fastapi


def generate_diagram() -> None:
    with Diagram(name="MyBookingServices", show=False):
        client = Client("client")

        vpn = VPN("Etna VPN")
        with Cluster("Manager"):
            with Cluster("Docker Services"):
                Docker("Registery")
                ingress = Traefik("Traefik")
                client >> vpn >> ingress

        with Cluster("Worker 1", direction="TB"):
            Gitlab("Gitlab")
            with Cluster("Docker Services"):
                with Cluster("app"):
                    app = Fastapi("API")
                    db = Mysql("Database")
                    ingress >> app >> db

        with Cluster("Worker2", direction="TB"):
            with Cluster("Docker Services"):
                with Cluster("app"):
                    app = Fastapi("API")
                    db = Mysql("Database")
                    ingress >> app >> db
                with Cluster("ELK Stack"):
                    elk = [
                        Kibana("Kibana"),
                        Elasticsearch("ES"),
                        Logstash("Logstash"),
                    ]

                    ingress >> elk[0]
                    elk[0] >> elk[1]
                    elk[0] >> elk[2]


if __name__ == '__main__':
    generate_diagram()
