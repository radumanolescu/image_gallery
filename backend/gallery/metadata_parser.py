"""
Shared TXT metadata parsing logic.

The legacy system stores one ``.txt`` file per image with ``KEY: VALUE``
lines. This module is used by ``load_metadata`` (import) and
``validate_metadata`` (migration accuracy check) so both parse files
identically.
"""
import datetime
import os

# Field name mapping from template to model fields
FIELD_MAPPING = {
    'Invent. Number': 'invent_number',
    'Invent. IMG-': 'invent_img',
    'Hig Res Image': 'high_res_image',
    'Date': 'date',
    'ID Title': 'id_title',
    'Website Title': 'website_title',
    'Part of a Gallery': 'part_of_gallery',
    'Medium': 'medium',
    'Substrate': 'substrate',
    'Dimensions HxWxD': 'dimensions_hxwxd',
    'Orientation': 'orientation',
    'Edition': 'edition',
    'Location': 'location',
    'in Inventory': 'in_inventory',
    'Number Sold': 'number_sold',
    'Sale Price': 'sale_price',
    'Cost of Goods': 'cost_of_goods',
    'Current Inventory': 'current_inventory',
    'Goods Sold': 'goods_sold',
    'Currently Shown': 'currently_shown',
    'Shown in Past': 'shown_in_past',
    'Keywords': 'keywords',
}

INT_FIELDS = ['number_sold', 'current_inventory']
FLOAT_FIELDS = ['sale_price', 'cost_of_goods', 'goods_sold']
DATE_FIELDS = ['date']


def parse_date(date_str):
    """Parse date string in various formats"""
    if not date_str or date_str == '.':
        return None

    formats = ['%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y']

    for fmt in formats:
        try:
            return datetime.datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue

    return None


def parse_txt_file(txt_file_path):
    """
    Parse a single metadata TXT file.

    Returns (metadata_dict, valid_metadata_found). The dict always contains
    'image_file_name' derived from the TXT filename.
    """
    txt_filename = os.path.basename(txt_file_path)
    image_file_name = txt_filename.replace('.txt', '.JPG')

    metadata_dict = {'image_file_name': image_file_name}
    valid_metadata_found = False

    with open(txt_file_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if not line or ':' not in line:
                continue

            parts = line.split(':', 1)  # Split on first colon only
            if len(parts) >= 2:
                field_name = parts[0].strip()
                field_value = parts[1].strip() if len(parts) > 1 else ''

                if field_name in FIELD_MAPPING:
                    model_field = FIELD_MAPPING[field_name]
                    valid_metadata_found = True

                    if model_field in INT_FIELDS:
                        try:
                            field_value = int(field_value) if field_value else None
                        except ValueError:
                            field_value = None
                    elif model_field in FLOAT_FIELDS:
                        try:
                            field_value = float(field_value) if field_value else None
                        except ValueError:
                            field_value = None
                    elif model_field in DATE_FIELDS:
                        field_value = parse_date(field_value)

                    metadata_dict[model_field] = field_value

    return metadata_dict, valid_metadata_found


def find_txt_files(path):
    """Recursively find all .txt files under path."""
    txt_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.txt'):
                txt_files.append(os.path.join(root, file))
    return txt_files
