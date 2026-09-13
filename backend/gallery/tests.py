import time
from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.test import APITestCase
from rest_framework import status


class DjangoConfigurationTests(TestCase):
    """Test Django project configuration settings"""

    def test_database_is_sqlite(self):
        """Test that SQLite is configured as the database"""
        self.assertEqual(settings.DATABASES['default']['ENGINE'], 'django.db.backends.sqlite3')

    def test_static_files_configured(self):
        """Test that static files are properly configured"""
        self.assertTrue(hasattr(settings, 'STATIC_URL'))
        self.assertTrue(hasattr(settings, 'STATIC_ROOT'))
        self.assertTrue(hasattr(settings, 'STATICFILES_DIRS'))

    def test_media_files_configured(self):
        """Test that media files are properly configured"""
        self.assertTrue(hasattr(settings, 'MEDIA_URL'))
        self.assertTrue(hasattr(settings, 'MEDIA_ROOT'))

    @override_settings(DEBUG=True)
    def test_debug_mode(self):
        """Test that debug mode can be enabled"""
        self.assertTrue(settings.DEBUG)

    def test_allowed_hosts(self):
        """Test that allowed hosts include localhost"""
        self.assertIn('localhost', settings.ALLOWED_HOSTS)
        self.assertIn('127.0.0.1', settings.ALLOWED_HOSTS)

    def test_installed_apps(self):
        """Test that required apps are installed"""
        required_apps = [
            'django.contrib.admin',
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'rest_framework',
            'gallery',
        ]
        for app in required_apps:
            self.assertIn(app, settings.INSTALLED_APPS)

    def test_rest_framework_configured(self):
        """Test that Django REST Framework is properly configured"""
        self.assertTrue(hasattr(settings, 'REST_FRAMEWORK'))
        self.assertIn('DEFAULT_AUTHENTICATION_CLASSES', settings.REST_FRAMEWORK)
        self.assertIn('DEFAULT_PERMISSION_CLASSES', settings.REST_FRAMEWORK)
        self.assertIn('DEFAULT_PAGINATION_CLASS', settings.REST_FRAMEWORK)


class AuthenticationTests(TestCase):
    """Test user authentication system"""

    def setUp(self):
        """Set up test user"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_creation(self):
        """Test that a user can be created"""
        self.assertEqual(User.objects.count(), 1)  # Only test user in test database
        self.assertTrue(self.user.check_password('testpass123'))

    def test_user_authentication(self):
        """Test that a user can authenticate"""
        from django.contrib.auth import authenticate
        authenticated_user = authenticate(username='testuser', password='testpass123')
        self.assertIsNotNone(authenticated_user)
        self.assertEqual(authenticated_user.username, 'testuser')

    def test_user_login_via_client(self):
        """Test user login using Django test client"""
        client = Client()
        # Try to access admin page (should redirect to login)
        response = client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/admin/login/'))

        # Create a superuser for admin access
        admin_user = User.objects.create_superuser(
            username='testadmin',
            email='testadmin@example.com',
            password='admin123'
        )

        # Login with superuser
        logged_in = client.login(username='testadmin', password='admin123')
        self.assertTrue(logged_in)

        # Access admin page after login
        response = client.get('/admin/')
        self.assertEqual(response.status_code, 200)

    def test_admin_user_exists(self):
        """Test that admin user can be created"""
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

    def test_user_password_validation(self):
        """Test that password validation is configured"""
        self.assertTrue(hasattr(settings, 'AUTH_PASSWORD_VALIDATORS'))
        self.assertTrue(len(settings.AUTH_PASSWORD_VALIDATORS) > 0)


class AdminInterfaceTests(TestCase):
    """Test Django admin interface"""

    def setUp(self):
        """Set up test data"""
        self.admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin_test@example.com',
            password='admin123'
        )
        self.client = Client()

    def test_admin_site_customization(self):
        """Test that admin site is customized"""
        from django.contrib import admin
        self.assertEqual(admin.site.site_header, "Image Gallery Admin")
        self.assertEqual(admin.site.site_title, "Image Gallery Admin Portal")
        self.assertEqual(admin.site.index_title, "Welcome to Image Gallery Administration")

    def test_admin_accessible_with_superuser(self):
        """Test that admin interface is accessible to superuser"""
        self.client.login(username='admin_test', password='admin123')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Image Gallery Admin")

    def test_admin_not_accessible_without_login(self):
        """Test that admin interface redirects without login"""
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/admin/login/'))

    def test_admin_user_management(self):
        """Test that users can be managed through admin"""
        self.client.login(username='admin_test', password='admin123')
        response = self.client.get('/admin/auth/user/')
        self.assertEqual(response.status_code, 200)


class RESTFrameworkTests(APITestCase):
    """Test Django REST Framework configuration"""

    def test_api_requires_authentication(self):
        """Test that API endpoints require authentication by default"""
        # This will be more relevant when we have actual API endpoints
        # For now, we test the configuration
        from rest_framework.settings import api_settings
        self.assertIsNotNone(api_settings.DEFAULT_AUTHENTICATION_CLASSES)
        self.assertIsNotNone(api_settings.DEFAULT_PERMISSION_CLASSES)

    def test_pagination_configured(self):
        """Test that pagination is configured"""
        from rest_framework.settings import api_settings
        self.assertIsNotNone(api_settings.DEFAULT_PAGINATION_CLASS)
        self.assertIsNotNone(api_settings.PAGE_SIZE)


class StaticAndMediaFilesTests(TestCase):
    """Test static and media files configuration"""

    def test_static_url_exists(self):
        """Test that static URL is configured"""
        self.assertTrue(settings.STATIC_URL.endswith('static/'))

    def test_media_url_exists(self):
        """Test that media URL is configured"""
        self.assertTrue(settings.MEDIA_URL.endswith('media/'))

    def test_static_root_is_path(self):
        """Test that static root is a valid path"""
        # Static root may not exist yet, but should be a valid path
        self.assertIsNotNone(settings.STATIC_ROOT)

    def test_media_root_is_path(self):
        """Test that media root is a valid path"""
        # Media root should point to the existing static/images directory
        self.assertIsNotNone(settings.MEDIA_ROOT)


class URLConfigurationTests(TestCase):
    """Test URL configuration"""

    def test_admin_url_exists(self):
        """Test that admin URL is configured"""
        from django.urls import reverse
        try:
            url = reverse('admin:index')
            self.assertEqual(url, '/admin/')
        except:
            # If reverse doesn't work, test the path directly
            client = Client()
            response = client.get('/admin/')
            self.assertIn(response.status_code, [200, 302])

    @override_settings(DEBUG=True)
    def test_static_files_served_in_debug(self):
        """Test that static files are served in debug mode"""
        client = Client()
        # This test will be more meaningful when we have actual static files
        # For now, we just verify the configuration
        self.assertTrue(settings.DEBUG)


class ImageMetadataModelTests(TestCase):
    """Test ImageMetadata model"""

    def setUp(self):
        """Set up test data"""
        from gallery.models import ImageMetadata
        self.metadata = ImageMetadata.objects.create(
            image_file_name='TEST_001.JPG',
            invent_number='INV001',
            id_title='Test Image',
            medium='watercolor',
            number_sold=5,
            sale_price=100.00
        )

    def test_metadata_creation(self):
        """Test that metadata can be created"""
        from gallery.models import ImageMetadata
        self.assertEqual(ImageMetadata.objects.count(), 1)
        self.assertEqual(self.metadata.image_file_name, 'TEST_001.JPG')
        self.assertEqual(self.metadata.id_title, 'Test Image')

    def test_metadata_str_representation(self):
        """Test string representation of metadata"""
        expected_str = 'TEST_001.JPG - Test Image'
        self.assertEqual(str(self.metadata), expected_str)

    def test_metadata_primary_key(self):
        """Test that image_file_name is the primary key"""
        from gallery.models import ImageMetadata
        self.assertEqual(self.metadata.pk, 'TEST_001.JPG')

    def test_metadata_update(self):
        """Test that metadata can be updated"""
        self.metadata.id_title = 'Updated Title'
        self.metadata.save()
        self.metadata.refresh_from_db()
        self.assertEqual(self.metadata.id_title, 'Updated Title')

    def test_metadata_fields(self):
        """Test that all expected fields exist"""
        from gallery.models import ImageMetadata
        # Check that the object has the expected fields
        self.assertTrue(hasattr(self.metadata, 'invent_number'))
        self.assertTrue(hasattr(self.metadata, 'medium'))
        self.assertTrue(hasattr(self.metadata, 'number_sold'))
        self.assertTrue(hasattr(self.metadata, 'sale_price'))
        self.assertTrue(hasattr(self.metadata, 'created_at'))
        self.assertTrue(hasattr(self.metadata, 'updated_at'))

    def test_metadata_null_fields(self):
        """Test that optional fields can be null"""
        from gallery.models import ImageMetadata
        metadata = ImageMetadata.objects.create(
            image_file_name='TEST_002.JPG'
        )
        self.assertIsNone(metadata.id_title)
        self.assertIsNone(metadata.medium)
        self.assertIsNone(metadata.number_sold)

    def test_metadata_timestamps(self):
        """Test that timestamps are automatically set"""
        self.assertIsNotNone(self.metadata.created_at)
        self.assertIsNotNone(self.metadata.updated_at)

    def test_metadata_update_timestamp(self):
        """Test that updated_at changes on save"""
        original_updated = self.metadata.updated_at
        self.metadata.id_title = 'New Title'
        self.metadata.save()
        self.metadata.refresh_from_db()
        self.assertGreater(self.metadata.updated_at, original_updated)

    def test_metadata_duplicate_key(self):
        """Test that duplicate primary keys are not allowed"""
        from gallery.models import ImageMetadata
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            ImageMetadata.objects.create(
                image_file_name='TEST_001.JPG',  # Same as setUp
                id_title='Duplicate'
            )


class DataLoadingTests(TestCase):
    """Test data loading functionality"""

    def setUp(self):
        """Set up test data"""
        from gallery.models import ImageMetadata
        import tempfile
        import os
        
        # Create a temporary directory for test TXT files
        self.temp_dir = tempfile.mkdtemp()
        
        # Create a sample TXT file
        self.sample_txt_path = os.path.join(self.temp_dir, 'TEST_IMG.txt')
        with open(self.sample_txt_path, 'w') as f:
            f.write('Invent. Number: INV001\n')
            f.write('ID Title: Test Image\n')
            f.write('Medium: watercolor\n')
            f.write('Number Sold: 5\n')
            f.write('Sale Price: 100.00\n')
            f.write('Date: 01/15/2023\n')

    def tearDown(self):
        """Clean up test data"""
        import shutil
        import os
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_load_metadata_command_exists(self):
        """Test that the load_metadata command exists"""
        from django.core.management import call_command
        from io import StringIO
        out = StringIO()
        try:
            call_command('load_metadata', '--help', stdout=out)
            self.assertIn('Load image metadata', out.getvalue())
        except:
            # Command exists if we can import it
            from gallery.management.commands.load_metadata import Command
            self.assertTrue(True)

    def test_load_metadata_dry_run(self):
        """Test that dry-run mode works without modifying database"""
        from django.core.management import call_command
        from gallery.models import ImageMetadata
        from io import StringIO
        
        out = StringIO()
        call_command('load_metadata', '--path', self.temp_dir, '--dry-run', stdout=out)
        
        # Should not create any records in dry-run mode
        self.assertEqual(ImageMetadata.objects.count(), 0)
        self.assertIn('DRY RUN', out.getvalue())

    def test_load_metadata_actual_load(self):
        """Test that actual loading creates database records"""
        from django.core.management import call_command
        from gallery.models import ImageMetadata
        from io import StringIO
        
        out = StringIO()
        call_command('load_metadata', '--path', self.temp_dir, stdout=out)
        
        # Should create one record
        self.assertEqual(ImageMetadata.objects.count(), 1)
        
        # Check the created record
        metadata = ImageMetadata.objects.get(image_file_name='TEST_IMG.JPG')
        self.assertEqual(metadata.invent_number, 'INV001')
        self.assertEqual(metadata.id_title, 'Test Image')
        self.assertEqual(metadata.medium, 'watercolor')
        self.assertEqual(metadata.number_sold, 5)
        self.assertEqual(float(metadata.sale_price), 100.00)

    def test_load_metadata_update_existing(self):
        """Test that loading updates existing records"""
        from django.core.management import call_command
        from gallery.models import ImageMetadata
        from io import StringIO
        
        # First load
        call_command('load_metadata', '--path', self.temp_dir)
        
        # Modify the TXT file
        with open(self.sample_txt_path, 'w') as f:
            f.write('Invent. Number: INV002\n')
            f.write('ID Title: Updated Title\n')
        
        # Second load
        out = StringIO()
        call_command('load_metadata', '--path', self.temp_dir, stdout=out)
        
        # Should still be one record, but updated
        self.assertEqual(ImageMetadata.objects.count(), 1)
        metadata = ImageMetadata.objects.get(image_file_name='TEST_IMG.JPG')
        self.assertEqual(metadata.invent_number, 'INV002')
        self.assertEqual(metadata.id_title, 'Updated Title')

    def test_load_metadata_clear_option(self):
        """Test that clear option removes existing data"""
        from django.core.management import call_command
        from gallery.models import ImageMetadata
        from io import StringIO
        
        # Create some initial data
        ImageMetadata.objects.create(image_file_name='OLD_IMG.JPG')
        
        # Load with clear option
        out = StringIO()
        call_command('load_metadata', '--path', self.temp_dir, '--clear', stdout=out)
        
        # Should only have the new data
        self.assertEqual(ImageMetadata.objects.count(), 1)
        self.assertIn('Cleared', out.getvalue())

    def test_load_metadata_invalid_file(self):
        """Test handling of invalid/malformed files"""
        from django.core.management import call_command
        from gallery.models import ImageMetadata
        import os
        from io import StringIO
        
        # Create an invalid TXT file (no colons, so no metadata will be extracted)
        invalid_path = os.path.join(self.temp_dir, 'INVALID.txt')
        with open(invalid_path, 'w') as f:
            f.write('Invalid content without colons\n')
        
        out = StringIO()
        call_command('load_metadata', '--path', self.temp_dir, stdout=out)
        
        # Should only process the valid file (invalid file should be skipped)
        self.assertEqual(ImageMetadata.objects.count(), 1)
        # Should report that the invalid file was skipped
        self.assertIn('Skipped', out.getvalue())

    def test_load_metadata_empty_directory(self):
        """Test handling of empty directory"""
        from django.core.management import call_command
        from gallery.models import ImageMetadata
        import tempfile
        import shutil
        from io import StringIO
        
        # Create empty directory
        empty_dir = tempfile.mkdtemp()
        
        try:
            out = StringIO()
            call_command('load_metadata', '--path', empty_dir, stdout=out)
            
            # Should not create any records
            self.assertEqual(ImageMetadata.objects.count(), 0)
            self.assertIn('No TXT files found', out.getvalue())
        finally:
            shutil.rmtree(empty_dir)

    def test_date_parsing(self):
        """Test date parsing functionality"""
        from gallery.metadata_parser import parse_date

        # Test various date formats
        self.assertEqual(parse_date('01/15/2023'),
                        parse_date('01/15/23'))
        self.assertIsNotNone(parse_date('2023-01-15'))
        self.assertIsNone(parse_date(''))
        self.assertIsNone(parse_date('.'))


class APITests(APITestCase):
    """Test REST API endpoints"""

    def setUp(self):
        """Set up test data"""
        from gallery.models import ImageMetadata
        
        # Create test metadata records
        self.metadata1 = ImageMetadata.objects.create(
            image_file_name='API_TEST_001.JPG',
            invent_number='API001',
            id_title='API Test Image 1',
            medium='watercolor',
            location='Gallery A',
            number_sold=3,
            sale_price=150.00
        )
        self.metadata2 = ImageMetadata.objects.create(
            image_file_name='API_TEST_002.JPG',
            invent_number='API002',
            id_title='API Test Image 2',
            medium='oil',
            location='Gallery B',
            number_sold=1,
            sale_price=250.00
        )
        
        # Create a test user for authenticated requests
        self.user = User.objects.create_user(
            username='apiuser',
            password='apipass123'
        )

    def test_list_images(self):
        """Test listing all images via API"""
        url = '/api/images/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['count'], 2)

    def test_list_images_unauthenticated_allowed(self):
        """Test that unauthenticated users can read (IsAuthenticatedOrReadOnly)"""
        url = '/api/images/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_image_detail(self):
        """Test retrieving a single image by primary key"""
        url = '/api/images/API_TEST_001.JPG/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['image_file_name'], 'API_TEST_001.JPG')
        self.assertEqual(response.data['id_title'], 'API Test Image 1')

    def test_retrieve_nonexistent_image(self):
        """Test retrieving a nonexistent image returns 404"""
        url = '/api/images/NONEXISTENT.JPG/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_image_requires_auth(self):
        """Test that creating an image requires authentication"""
        url = '/api/images/'
        data = {
            'image_file_name': 'API_TEST_003.JPG',
            'id_title': 'New API Image',
            'medium': 'acrylic'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_image_authenticated(self):
        """Test creating an image with authentication"""
        self.client.force_authenticate(user=self.user)
        url = '/api/images/'
        data = {
            'image_file_name': 'API_TEST_003.JPG',
            'id_title': 'New API Image',
            'medium': 'acrylic'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['image_file_name'], 'API_TEST_003.JPG')

    def test_update_image_authenticated(self):
        """Test updating an image with authentication"""
        self.client.force_authenticate(user=self.user)
        url = '/api/images/API_TEST_001.JPG/'
        data = {'id_title': 'Updated Title'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id_title'], 'Updated Title')

    def test_delete_image_authenticated(self):
        """Test deleting an image with authentication"""
        self.client.force_authenticate(user=self.user)
        url = '/api/images/API_TEST_002.JPG/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        from gallery.models import ImageMetadata
        self.assertFalse(
            ImageMetadata.objects.filter(image_file_name='API_TEST_002.JPG').exists()
        )

    def test_filter_by_medium(self):
        """Test filtering images by medium"""
        url = '/api/images/?medium=watercolor'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['medium'], 'watercolor'
        )

    def test_search_functionality(self):
        """Test full-text search across metadata fields"""
        url = '/api/images/?search=watercolor'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_search_by_title(self):
        """Test search by image title"""
        url = '/api/images/?search=Test Image 2'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['id_title'], 'API Test Image 2'
        )

    def test_ordering_by_field(self):
        """Test ordering results by field"""
        url = '/api/images/?ordering=sale_price'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        self.assertEqual(results[0]['image_file_name'], 'API_TEST_001.JPG')
        self.assertEqual(results[1]['image_file_name'], 'API_TEST_002.JPG')

    def test_pagination(self):
        """Test that results are paginated"""
        # Create more records to test pagination
        from gallery.models import ImageMetadata
        for i in range(25):
            ImageMetadata.objects.create(
                image_file_name=f'PAGE_TEST_{i:03d}.JPG',
                id_title=f'Page Test {i}'
            )
        
        url = '/api/images/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertEqual(len(response.data['results']), 20)  # PAGE_SIZE

    def test_bulk_update_requires_auth(self):
        """Test that bulk update requires authentication"""
        url = '/api/images/bulk_update/'
        data = {
            'image_file_names': ['API_TEST_001.JPG'],
            'updates': {'location': 'Updated Location'}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bulk_update_authenticated(self):
        """Test bulk update with authentication"""
        self.client.force_authenticate(user=self.user)
        url = '/api/images/bulk_update/'
        data = {
            'image_file_names': ['API_TEST_001.JPG', 'API_TEST_002.JPG'],
            'updates': {'location': 'Bulk Updated Gallery'}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['updated_count'], 2)
        
        # Verify the update was applied
        from gallery.models import ImageMetadata
        img1 = ImageMetadata.objects.get(image_file_name='API_TEST_001.JPG')
        self.assertEqual(img1.location, 'Bulk Updated Gallery')

    def test_bulk_update_invalid_fields_ignored(self):
        """Test that invalid fields are ignored in bulk update"""
        self.client.force_authenticate(user=self.user)
        url = '/api/images/bulk_update/'
        data = {
            'image_file_names': ['API_TEST_001.JPG'],
            'updates': {'invalid_field': 'value', 'location': 'Valid'}
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify only valid field was updated
        from gallery.models import ImageMetadata
        img = ImageMetadata.objects.get(image_file_name='API_TEST_001.JPG')
        self.assertEqual(img.location, 'Valid')
        self.assertFalse(hasattr(img, 'invalid_field'))

    def test_export_csv(self):
        """Test CSV export endpoint"""
        url = '/api/images/export_csv/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertIn('attachment', response['Content-Disposition'])

    def test_export_excel(self):
        """Test Excel export endpoint"""
        url = '/api/images/export_excel/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('spreadsheetml', response['Content-Type'])

    def test_export_pdf(self):
        """Test PDF export endpoint"""
        url = '/api/images/export_pdf/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/pdf')

    def test_api_docs_endpoint(self):
        """Test that API documentation endpoint is accessible"""
        url = '/api/schema/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_swagger_ui_endpoint(self):
        """Test that Swagger UI is accessible"""
        url = '/api/docs/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_by_part_of_gallery(self):
        """Search must cover part_of_gallery (gallery names like 'Alien Worlds')"""
        from gallery.models import ImageMetadata
        ImageMetadata.objects.create(
            image_file_name='GALLERY_TEST.JPG',
            id_title='Gallery Test',
            part_of_gallery='Alian Worlds'
        )
        response = self.client.get('/api/images/?search=Alian Worlds')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(
            response.data['results'][0]['image_file_name'], 'GALLERY_TEST.JPG'
        )

    def test_filter_options_endpoint(self):
        """filter_options returns distinct values across the whole collection"""
        from gallery.models import ImageMetadata
        ImageMetadata.objects.create(
            image_file_name='OPT_TEST.JPG',
            medium='encaustic',
            part_of_gallery='Rare Gallery'
        )
        response = self.client.get('/api/images/filter_options/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('medium', response.data)
        self.assertIn('part_of_gallery', response.data)
        self.assertIn('encaustic', response.data['medium'])
        self.assertIn('Rare Gallery', response.data['part_of_gallery'])
        self.assertIn('watercolor', response.data['medium'])


class AuthEndpointTests(APITestCase):
    """Test authentication endpoints"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='authuser',
            password='authpass123'
        )

    def test_csrf_endpoint_sets_cookie(self):
        """Test that the CSRF endpoint sets a cookie"""
        response = self.client.get('/api/auth/csrf/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('csrftoken', response.cookies)

    def test_login_success(self):
        """Test successful login"""
        response = self.client.post('/api/auth/login/', {
            'username': 'authuser',
            'password': 'authpass123'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'authuser')

    def test_login_invalid_credentials(self):
        """Test login with wrong password"""
        response = self.client.post('/api/auth/login/', {
            'username': 'authuser',
            'password': 'wrongpass'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_me_unauthenticated(self):
        """Test /me endpoint when not logged in"""
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_authenticated(self):
        """Test /me endpoint when logged in"""
        self.client.login(username='authuser', password='authpass123')
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'authuser')

    def test_logout(self):
        """Test logout ends the session"""
        self.client.login(username='authuser', password='authpass123')
        response = self.client.post('/api/auth/logout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify logged out
        response = self.client.get('/api/auth/me/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_session_persists_for_writes(self):
        """Test that a session login enables write operations"""
        self.client.login(username='authuser', password='authpass123')
        from gallery.models import ImageMetadata
        response = self.client.post('/api/images/', {
            'image_file_name': 'AUTH_TEST.JPG',
            'id_title': 'Auth Test'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class PerformanceTests(APITestCase):
    """Performance smoke tests with a larger dataset.

    Time bounds are generous — these catch pathological regressions
    (N+1 queries, missing pagination) rather than measure precise latency.
    """

    RECORD_COUNT = 300

    @classmethod
    def setUpTestData(cls):
        from gallery.models import ImageMetadata
        ImageMetadata.objects.bulk_create([
            ImageMetadata(
                image_file_name=f'PERF_{i:04d}.JPG',
                id_title=f'Performance Test Image {i}',
                medium='watercolor' if i % 2 == 0 else 'oil',
                location='Test Gallery',
                number_sold=i % 10,
                sale_price=100 + i,
            )
            for i in range(cls.RECORD_COUNT)
        ])

    def test_list_endpoint_responds_quickly(self):
        start = time.time()
        response = self.client.get('/api/images/')
        elapsed = time.time() - start
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.RECORD_COUNT)
        self.assertLess(elapsed, 5.0, f'List too slow: {elapsed:.2f}s')

    def test_search_endpoint_responds_quickly(self):
        start = time.time()
        response = self.client.get('/api/images/?search=watercolor')
        elapsed = time.time() - start
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], self.RECORD_COUNT // 2)
        self.assertLess(elapsed, 5.0, f'Search too slow: {elapsed:.2f}s')

    def test_csv_export_responds_quickly(self):
        start = time.time()
        response = self.client.get('/api/images/export_csv/')
        elapsed = time.time() - start
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Header + one row per record
        self.assertEqual(
            len(response.content.decode().strip().splitlines()),
            self.RECORD_COUNT + 1
        )
        self.assertLess(elapsed, 10.0, f'CSV export too slow: {elapsed:.2f}s')

    def test_pagination_scales(self):
        response = self.client.get('/api/images/?page=10')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 20)
        self.assertEqual(response.data['count'], self.RECORD_COUNT)


class SecurityTests(APITestCase):
    """Security-focused API tests"""

    def setUp(self):
        from gallery.models import ImageMetadata
        ImageMetadata.objects.create(
            image_file_name='SEC_001.JPG', id_title='Security Test'
        )
        self.user = User.objects.create_user(
            username='secuser', password='secpass123'
        )

    def test_update_requires_auth(self):
        response = self.client.patch(
            '/api/images/SEC_001.JPG/', {'id_title': 'X'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_requires_auth(self):
        response = self.client.delete('/api/images/SEC_001.JPG/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bulk_import_requires_auth(self):
        csv_file = SimpleUploadedFile(
            'data.csv', b'image_file_name\nX.JPG\n', content_type='text/csv'
        )
        response = self.client.post(
            '/api/images/bulk_import/', {'file': csv_file}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_csrf_enforced_for_session_authenticated_writes(self):
        """Session-authenticated POST without CSRF token must be rejected."""
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(username='secuser', password='secpass123')
        response = csrf_client.post(
            '/api/images/',
            data='{"image_file_name": "CSRF_TEST.JPG"}',
            content_type='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_csrf_allows_request_with_valid_token(self):
        """Session-authenticated POST with the CSRF token succeeds."""
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.login(username='secuser', password='secpass123')
        # Prime the CSRF cookie
        csrf_client.get('/api/auth/csrf/')
        token = csrf_client.cookies['csrftoken'].value
        response = csrf_client.post(
            '/api/images/',
            data='{"image_file_name": "CSRF_OK.JPG"}',
            content_type='application/json',
            HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_bulk_import_rejects_unsupported_file_type(self):
        self.client.force_authenticate(user=self.user)
        bad_file = SimpleUploadedFile(
            'malware.exe', b'MZ\x90\x00', content_type='application/octet-stream'
        )
        response = self.client.post(
            '/api/images/bulk_import/', {'file': bad_file}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Unsupported file format', str(response.data))

    def test_bulk_import_rejects_missing_file(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/images/bulk_import/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_bulk_import_csv(self):
        self.client.force_authenticate(user=self.user)
        csv_file = SimpleUploadedFile(
            'data.csv',
            b'image_file_name,id_title,medium\nIMP_001.JPG,Imported,oil\n',
            content_type='text/csv',
        )
        response = self.client.post(
            '/api/images/bulk_import/', {'file': csv_file}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['imported_count'], 1)

    def test_search_handles_sql_injection_attempt(self):
        response = self.client.get(
            "/api/images/?search='; DROP TABLE image_metadata; --"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_ordering_field_ignored(self):
        response = self.client.get('/api/images/?ordering=hacked_field')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_rejects_empty_body(self):
        response = self.client.post('/api/auth/login/', {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MigrationValidationTests(TestCase):
    """Test the validate_metadata management command"""

    def setUp(self):
        import tempfile
        import os
        self.temp_dir = tempfile.mkdtemp()
        txt_path = os.path.join(self.temp_dir, 'VAL_IMG.txt')
        with open(txt_path, 'w') as f:
            f.write('Invent. Number: V001\n')
            f.write('ID Title: Validation Image\n')
            f.write('Medium: acrylic\n')
            f.write('Number Sold: 2\n')

    def tearDown(self):
        import shutil
        import os
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_validate_reports_matching_records(self):
        """Loaded records validate cleanly against their TXT files"""
        from django.core.management import call_command
        from io import StringIO
        call_command('load_metadata', f'--path={self.temp_dir}')
        out = StringIO()
        call_command('validate_metadata', f'--path={self.temp_dir}', stdout=out)
        output = out.getvalue()
        self.assertIn('Fully matching:         1', output)
        self.assertIn('All records validated successfully', output)

    def test_validate_reports_missing_record(self):
        """A TXT file with no DB record is reported as missing"""
        from django.core.management import call_command
        from io import StringIO
        out = StringIO()
        call_command('validate_metadata', f'--path={self.temp_dir}', stdout=out)
        output = out.getvalue()
        self.assertIn('Missing DB records:', output)
        self.assertIn('VAL_IMG.JPG', output)

    def test_validate_reports_field_mismatch(self):
        """A DB record that differs from its TXT file is reported"""
        from django.core.management import call_command
        from gallery.models import ImageMetadata
        from io import StringIO
        call_command('load_metadata', f'--path={self.temp_dir}')
        ImageMetadata.objects.filter(
            image_file_name='VAL_IMG.JPG'
        ).update(medium='watercolor')
        out = StringIO()
        call_command('validate_metadata', f'--path={self.temp_dir}', stdout=out)
        output = out.getvalue()
        self.assertIn('mismatch', output.lower())
        self.assertIn('medium', output)
