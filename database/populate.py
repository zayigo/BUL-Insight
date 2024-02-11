from database.schema import Metric, MetricCategory, Region
from pdf_schema import SCHEMA

regions = [
    "Abruzzo",
    "Basilicata",
    "Calabria",
    "Campania",
    "Emilia Romagna",
    "Friuli Venezia Giulia",
    "Lazio",
    "Liguria",
    "Lombardia",
    "Marche",
    "Molise",
    "Piemonte",
    "Puglia",
    "Sardegna",
    "Sicilia",
    "Toscana",
    "Trentino Alto Adige",
    "Umbria",
    "Valle d'Aosta",
    "Veneto"
]


def populate_metrics():
    for table_name, categories in SCHEMA.items():
        for category_name, metrics in categories.items():
            category, created = MetricCategory.get_or_create(name=category_name)
            for metric_name in metrics:
                Metric.get_or_create(name=metric_name, category=category)


def populate_regions():
    for region_name in regions:
        Region.get_or_create(name=region_name)
