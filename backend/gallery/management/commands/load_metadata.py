import os
import re
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from gallery.models import ImageMetadata


class Command(BaseCommand):
    help = 'Load image metadata from TXT files into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='Path to directory containing TXT files (default: MEDIA_ROOT)',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing metadata before loading',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Simulate loading without actually modifying the database',
        )

    def handle(self, *args, **options):
        # Determine the path to scan for TXT files
        path = options.get('path') or settings.MEDIA_ROOT
        
        if not os.path.exists(path):
            raise CommandError(f'Path does not exist: {path}')

        clear_existing = options.get('clear', False)
        dry_run = options.get('dry_run', False)

        if clear_existing:
            if dry_run:
                self.stdout.write(self.style.WARNING('DRY RUN: Would clear existing metadata'))
            else:
                count = ImageMetadata.objects.count()
                ImageMetadata.objects.all().delete()
                self.stdout.write(self.style.WARNING(f'Cleared {count} existing metadata records'))

        # Field name mapping from template to model fields
        field_mapping = {
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

        # Data type handling
        int_fields = ['number_sold', 'current_inventory']
        float_fields = ['sale_price', 'cost_of_goods', 'goods_sold']
        date_fields = ['date']

        # Find all TXT files
        txt_files = []
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith('.txt'):
                    txt_files.append(os.path.join(root, file))

        if not txt_files:
            self.stdout.write(self.style.WARNING('No TXT files found in the specified path'))
            return

        self.stdout.write(f'Found {len(txt_files)} TXT files to process')

        # Process each TXT file
        success_count = 0
        error_count = 0
        errors = []

        for txt_file_path in txt_files:
            try:
                # Extract image file name from TXT file name
                txt_filename = os.path.basename(txt_file_path)
                image_file_name = txt_filename.replace('.txt', '.JPG')
                
                if not os.path.exists(txt_file_path):
                    self.stdout.write(self.style.WARNING(f'TXT file not found: {txt_file_path}'))
                    error_count += 1
                    continue

                # Parse the TXT file
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
                            
                            # Map field name to model field
                            if field_name in field_mapping:
                                model_field = field_mapping[field_name]
                                valid_metadata_found = True
                                
                                # Handle data type conversions
                                if model_field in int_fields:
                                    try:
                                        field_value = int(field_value) if field_value else None
                                    except ValueError:
                                        field_value = None
                                elif model_field in float_fields:
                                    try:
                                        field_value = float(field_value) if field_value else None
                                    except ValueError:
                                        field_value = None
                                elif model_field in date_fields:
                                    field_value = self.parse_date(field_value)
                                
                                metadata_dict[model_field] = field_value

                # Skip files with no valid metadata
                if not valid_metadata_found:
                    self.stdout.write(self.style.WARNING(f'Skipped {image_file_name}: No valid metadata found'))
                    continue

                # Create or update the record
                if dry_run:
                    self.stdout.write(f'DRY RUN: Would process {image_file_name}')
                    success_count += 1
                else:
                    obj, created = ImageMetadata.objects.update_or_create(
                        image_file_name=image_file_name,
                        defaults=metadata_dict
                    )
                    action = 'Created' if created else 'Updated'
                    self.stdout.write(f'{action}: {image_file_name}')
                    success_count += 1

            except Exception as e:
                error_msg = f'Error processing {txt_file_path}: {str(e)}'
                self.stdout.write(self.style.ERROR(error_msg))
                errors.append(error_msg)
                error_count += 1

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(f'Total files processed: {len(txt_files)}')
        self.stdout.write(self.style.SUCCESS(f'Successfully processed: {success_count}'))
        self.stdout.write(self.style.ERROR(f'Errors: {error_count}'))

        if errors:
            self.stdout.write('\nErrors encountered:')
            for error in errors:
                self.stdout.write(self.style.ERROR(f'  - {error}'))

        if not dry_run:
            self.stdout.write(f'\nTotal metadata records in database: {ImageMetadata.objects.count()}')

    def parse_date(self, date_str):
        """Parse date string in various formats"""
        if not date_str or date_str == '.':
            return None
        
        formats = ['%m/%d/%Y', '%m/%d/%y', '%Y-%m-%d', '%d/%m/%Y', '%d/%m/%y']
        
        for fmt in formats:
            try:
                return datetime.datetime.strptime(date_str, fmt).date()
            except ValueError:
                continue
        
        # If no format matches, return None
        return None