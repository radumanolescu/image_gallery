import os
import decimal
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from gallery.models import ImageMetadata
from gallery.metadata_parser import find_txt_files, parse_txt_file


class Command(BaseCommand):
    help = (
        'Validate migration accuracy: re-parse every TXT metadata file and '
        'compare each field against the database record.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            type=str,
            help='Path to directory containing TXT files (default: MEDIA_ROOT)',
        )

    def handle(self, *args, **options):
        path = options.get('path') or settings.MEDIA_ROOT

        if not os.path.exists(path):
            raise CommandError(f'Path does not exist: {path}')

        txt_files = find_txt_files(path)
        if not txt_files:
            self.stdout.write(self.style.WARNING('No TXT files found in the specified path'))
            return

        self.stdout.write(f'Validating {len(txt_files)} TXT files against the database...')

        checked = 0
        matched = 0
        missing_records = []
        mismatches = []
        skipped = []
        errors = []

        for txt_file_path in txt_files:
            try:
                metadata_dict, valid_metadata_found = parse_txt_file(txt_file_path)
                image_file_name = metadata_dict['image_file_name']

                if not valid_metadata_found:
                    skipped.append(image_file_name)
                    continue

                checked += 1

                try:
                    record = ImageMetadata.objects.get(image_file_name=image_file_name)
                except ImageMetadata.DoesNotExist:
                    missing_records.append(image_file_name)
                    continue

                field_diffs = []
                for field, expected in metadata_dict.items():
                    if field == 'image_file_name':
                        continue
                    actual = getattr(record, field)
                    if not self._values_equal(expected, actual):
                        field_diffs.append(
                            f'{field}: TXT={expected!r} DB={actual!r}'
                        )

                if field_diffs:
                    mismatches.append((image_file_name, field_diffs))
                else:
                    matched += 1

            except Exception as e:
                errors.append(f'{txt_file_path}: {e}')

        # DB records with no corresponding TXT file
        txt_image_names = {
            os.path.basename(f).replace('.txt', '.JPG') for f in txt_files
        }
        orphan_records = list(
            ImageMetadata.objects.exclude(image_file_name__in=txt_image_names)
            .values_list('image_file_name', flat=True)
        )

        # Report
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write('MIGRATION VALIDATION REPORT')
        self.stdout.write('=' * 60)
        self.stdout.write(f'TXT files found:        {len(txt_files)}')
        self.stdout.write(f'Records checked:        {checked}')
        self.stdout.write(self.style.SUCCESS(f'Fully matching:         {matched}'))

        if skipped:
            self.stdout.write(self.style.WARNING(
                f'Skipped (no metadata):  {len(skipped)}'
            ))
            for name in skipped[:20]:
                self.stdout.write(f'  - {name}')

        if missing_records:
            self.stdout.write(self.style.ERROR(
                f'Missing DB records:     {len(missing_records)}'
            ))
            for name in missing_records[:20]:
                self.stdout.write(f'  - {name}')

        if mismatches:
            self.stdout.write(self.style.ERROR(
                f'Records with mismatches: {len(mismatches)}'
            ))
            for name, diffs in mismatches[:20]:
                self.stdout.write(f'  - {name}')
                for d in diffs:
                    self.stdout.write(f'      {d}')

        if orphan_records:
            self.stdout.write(self.style.WARNING(
                f'DB records w/o TXT file: {len(orphan_records)}'
            ))
            for name in orphan_records[:20]:
                self.stdout.write(f'  - {name}')

        if errors:
            self.stdout.write(self.style.ERROR(f'Parse errors:           {len(errors)}'))
            for e in errors[:20]:
                self.stdout.write(f'  - {e}')

        if matched == checked and not missing_records and not errors:
            self.stdout.write(self.style.SUCCESS(
                '\nAll records validated successfully.'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                '\nValidation completed with differences (see above).'
            ))

    @staticmethod
    def _values_equal(expected, actual):
        """Compare a parsed TXT value against a DB field value."""
        if expected is None and actual is None:
            return True
        if expected is None or actual is None:
            return False
        if isinstance(actual, decimal.Decimal):
            try:
                return decimal.Decimal(str(expected)) == actual
            except decimal.InvalidOperation:
                return False
        return expected == actual
