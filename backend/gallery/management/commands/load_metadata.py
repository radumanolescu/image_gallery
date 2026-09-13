import os
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from gallery.models import ImageMetadata
from gallery.metadata_parser import find_txt_files, parse_txt_file


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

        # Find all TXT files
        txt_files = find_txt_files(path)

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
                metadata_dict, valid_metadata_found = parse_txt_file(txt_file_path)
                image_file_name = metadata_dict['image_file_name']

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
