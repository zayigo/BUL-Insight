import argparse
import calendar
import os

from database.export import export_data
from database.schema import MetricCategory
from doc_parser import DocParser
from pdf_schema import SCHEMA, SCHEMA_EXCEPTIONS

# Setup command line argument parsing
args_parser = argparse.ArgumentParser(description="Process PDF files for data extraction")
args_parser.add_argument("--file", type=str, help="Specify a single PDF file name for processing")
args_parser.add_argument("--folder", type=str, help="Specify the folder path to process all PDF files within")
args_parser.add_argument("--export", action="store_true", help="Export the processed data")
args_parser.add_argument(
    "--export-dir", type=str, required=False, help="Specify the export directory for processed data"
)
args = args_parser.parse_args()

# Validate that --export-dir is provided if --export is set
if args.export and not args.export_dir:
    args_parser.error("--export-dir is required when --export is set")
else:
    print("Starting PDF processing..")

pdf_files = []
if args.file:
    pdf_files.append(args.file)
    print(f"Processing single file: {args.file}")
elif args.folder:
    pdf_files = [f for f in os.listdir(args.folder) if f.endswith('.pdf')]
    print(f"Processing all PDF files in folder: {args.folder}")

for file_name in pdf_files:
    print(f"Processing file: {file_name}")
    base_file_name = os.path.basename(file_name)
    pdf_path = os.path.join(args.folder, file_name) if args.folder else file_name
    doc_parser = DocParser(pdf_path)
    section_ranges = doc_parser.find_section_ranges()
    section_tables = doc_parser.find_section_tables(section_ranges)

    for section_title, tables_info in section_tables.items():
        categories = list(SCHEMA[section_title].keys())
        current_category = None
        regions_found = 0

        for table in tables_info:
            df = table[2]  # Extract the DataFrame from the tuple

            # All regions of the last category have been found
            if not categories and regions_found == 20:
                break

            if categories and (current_category is None or regions_found == 20):
                category_name = categories.pop(0)
                current_category = MetricCategory.get(MetricCategory.name == category_name)
                regions_found = 0
                if (base_file_name == '2020_04.pdf'  #
                        and section_title == 'AVVIO DEI CANTIERI'  # noqa
                        and current_category.name == 'Esecuzione dei cantieri FTTH'):  # noqa
                    regions_found += 2
                    print(f"Special handling for {section_title} in {file_name}")
                print(f"Processing category: {section_title}-{current_category.name}")
            # elif not categories:
            #     print('No more categories to process')
            #     break

            columns = SCHEMA[section_title][current_category.name]

            # Handle schema exceptions
            if (base_file_name in {'2022_06.pdf', '2022_07.pdf', '2022_08.pdf', '2022_09.pdf'}  #
                    and section_title == 'UNITA’ IMMOBILIARI'  # noqa
                    and current_category.name == 'Unita immobiliari'):  # noqa
                columns = SCHEMA_EXCEPTIONS[section_title][current_category.name]
                print(f"Applying schema exception for {section_title} in {file_name}")

            base_name = os.path.basename(doc_parser.document_path)
            year, month = base_name.split('_')[0], base_name.split('_')[1].split('.')[0]
            last_day = calendar.monthrange(int(year), int(month))[1]
            date_str = f"{year}-{month.zfill(2)}-{str(last_day).zfill(2)}"
            try:
                regions_found += doc_parser.process_table(df, columns, date_str, current_category)
                print(f"Successfully processed table for {current_category.name}")
            except ValueError as e:
                print(f"Error processing table: {e}")

# Data export condition
if args.export and args.export_dir:
    print(f"Exporting processed data to {args.export_dir}")
    export_data(args.export_dir)
