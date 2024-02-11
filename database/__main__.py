from database.populate import populate_metrics, populate_regions
from database.schema import Metric, MetricCategory, MonthlyData, Region, db

if __name__ == "__main__":
    db.connect()
    db.create_tables([Region, Metric, MonthlyData, MetricCategory])
    populate_metrics()
    populate_regions()
