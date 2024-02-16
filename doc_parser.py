import camelot
import fitz  # PyMuPDF
from peewee import fn

from database.schema import Metric, MonthlyData, Region
from pdf_schema import SCHEMA


class DocParser:
    def __init__(self, document_path, page_height=842, page_width=595):
        self.document_path = document_path
        self.section_titles = list(SCHEMA.keys())
        self.page_height = page_height
        self.page_width = page_width

    def find_section_ranges(self):
        doc = fitz.open(self.document_path)
        sections = {title: {'start': None, 'end': None} for title in self.section_titles}
        current_section = None

        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            lines = text.split('\n')
            for line in lines:
                for title in self.section_titles:
                    if title in line:
                        if text_instances := page.search_for(title):
                            coords = text_instances[0]
                        else:
                            coords = None
                        if current_section and sections[current_section]['end'] is None:
                            sections[current_section]['end'] = page_num + 1
                            sections[current_section]['end_coords'] = coords
                        current_section = title
                        if sections[current_section]['start'] is None:
                            sections[current_section]['start'] = page_num + 1
                            sections[current_section]['start_coords'] = coords
                        break
        return sections

    def find_section_tables(self, section_ranges):
        section_tables = {}
        for section, range_info in section_ranges.items():
            if range_info['start'] is None:
                continue
            section_tables.setdefault(section, [])
            range_info['end'] = range_info['end'] or range_info['start']
            y_start = self.page_height - range_info.get('start_coords', [0, self.page_height, 0, 0])[1]
            y_end = self.page_height - range_info.get('end_coords', [0, 0, 0, self.page_height])[3]
            is_single_page = range_info['end'] == range_info['start']
            page_range = f"{range_info['start']}" if is_single_page else f"{range_info['start']}-{range_info['end']}"
            if is_single_page:
                table_regions = [f"0,{y_start},{self.page_width},{y_end}"]
            else:
                table_regions = [f"0,{y_start},{self.page_width},0", f"0,{self.page_height},{self.page_width},{y_end}"]
            extracted_tables = []
            for page, region in zip(page_range.split('-'), table_regions):
                tables = camelot.read_pdf(
                    self.document_path,
                    strip_text='\n',
                    flavor='lattice',
                    pages=page,
                    table_regions=[region],
                    backend="ghostscript"
                )
                for table in tables:
                    page_order = table.parsing_report['order']
                    page_number = table.parsing_report['page']
                    extracted_tables.append((page_number, page_order, table.df))
            if '-' in page_range and int(range_info['end']) - int(range_info['start']) > 1:
                page_range = f"{int(range_info['start']) + 1}-{int(range_info['end']) - 1}"
                tables_middle = camelot.read_pdf(
                    self.document_path, strip_text='\n', flavor='lattice', pages=page_range, backend="ghostscript"
                )
                for table in tables_middle:
                    page_order = table.parsing_report['order']
                    page_number = table.parsing_report['page']
                    extracted_tables.append((page_number, page_order, table.df))
            extracted_tables.sort(key=lambda x: (x[0], x[1]))
            section_tables[section] = extracted_tables
        return section_tables

    def process_table(self, table, columns, date, current_category):
        if len(table.columns) != len(columns) + 1:
            raise ValueError("The structure of the table does not match the expected schema")
        regions_found = 0
        for index, row in table.iterrows():
            region_name = row[0].replace('’', '\'').replace('-', ' ').strip().lower()
            if not region_name or region_name in ['totale complessivo', 'regione']:
                continue
            try:
                region = Region.get(fn.lower(Region.name) == region_name)
                regions_found += 1
            except Region.DoesNotExist:
                print(f"Region {region_name} not found in database")
                continue
            for col_index, metric_name in enumerate(columns, start=1):
                try:
                    metric_value = float(row[col_index].replace('-', '').replace('.', '').strip())
                except ValueError:
                    metric_value = None
                try:
                    metric = Metric.get((Metric.category == current_category) & (Metric.name == metric_name))
                    try:
                        monthly_data = MonthlyData.get(region=region.id, metric_date=date, metric=metric.id)
                        monthly_data.value = metric_value
                        monthly_data.save()
                        print(f"Updated monthly data for metric '{metric_name}', region '{region.id}', date '{date}'")
                    except MonthlyData.DoesNotExist:
                        MonthlyData.create(region=region.id, value=metric_value, metric_date=date, metric=metric.id)
                        print(
                            f"Created new monthly data for metric '{metric_name}', region '{region.id}', date '{date}'"
                        )
                except Metric.DoesNotExist:
                    print(f"Metric '{metric_name}' not found for category '{current_category}'")
        return regions_found
