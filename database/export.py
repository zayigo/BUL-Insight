import csv

from database.schema import Metric, MetricCategory, MonthlyData, Region


def export_data(csv_path):
    regions = Region.select()
    for r in regions:
        filename = f"{csv_path}/{r.name.lower().replace(' ', '_')}.csv"
        with open(filename, 'w', newline='') as csvfile:
            metrics = Metric.select()
            fieldnames = ['mese'] + [f"{m.category.name}-{m.name}" for m in metrics]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            # Fetch all data for the region, then sort it by metric_date
            all_data = MonthlyData.select().where(MonthlyData.region == r.id).order_by(MonthlyData.metric_date.asc())
            # Group data by month
            data_by_month = {}
            for d in all_data:
                month_key = d.metric_date.strftime('%Y-%m-%d')
                if month_key not in data_by_month:
                    data_by_month[month_key] = {}
                for m in metrics:
                    if d.metric_id == m.id:
                        data_by_month[month_key][f"{m.category.name}-{m.name}"] = d.value
            # Write data rows
            for month, metrics_values in data_by_month.items():
                row = {'mese': month}
                for m in metrics:
                    metric_key = f"{m.category.name}-{m.name}"
                    row[metric_key] = metrics_values.get(metric_key, None)
                writer.writerow(row)


def export_cumulative_data_avvio_servizi(csv_path):
    category_name = "Avvio dei servizi"
    category = MetricCategory.select().where(MetricCategory.name == category_name).get()
    metrics = Metric.select().where(Metric.category == category)
    filename = f"{csv_path}/cumulative_{category_name.lower().replace(' ', '_')}.csv"
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['mese'] + [f"{m.category.name}-{m.name}" for m in metrics]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        # Fetch all data for the specified category, then sort it by metric_date
        all_data = MonthlyData.select().join(Metric).where(Metric.category == category).order_by(
            MonthlyData.metric_date.asc()
        )
        # Group data by month
        data_by_month = {}
        for d in all_data:
            if d.value == '-':
                continue
            month_key = d.metric_date.strftime('%Y-%m-%d')
            if month_key not in data_by_month:
                data_by_month[month_key] = {}
            for m in metrics:
                if d.metric_id == m.id:
                    data_by_month[month_key][f"{m.category.name}-{m.name}"] = data_by_month[month_key].get(
                        f"{m.category.name}-{m.name}", 0
                    ) + d.value
        # Write data rows
        for month, metrics_values in data_by_month.items():
            row = {'mese': month}
            for m in metrics:
                metric_key = f"{m.category.name}-{m.name}"
                row[metric_key] = metrics_values.get(metric_key, None)
            writer.writerow(row)
