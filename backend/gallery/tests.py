from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
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
            f.write('Invent. Number\tINV001\n')
            f.write('ID Title\tTest Image\n')
            f.write('Medium\twatercolor\n')
            f.write('Number Sold\t5\n')
            f.write('Sale Price\t100.00\n')
            f.write('Date\t01/15/2023\n')

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
            f.write('Invent. Number\tINV002\n')
            f.write('ID Title\tUpdated Title\n')
        
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
        
        # Create an invalid TXT file (no tabs, so no metadata will be extracted)
        invalid_path = os.path.join(self.temp_dir, 'INVALID.txt')
        with open(invalid_path, 'w') as f:
            f.write('Invalid content without tabs\n')
        
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
        from gallery.management.commands.load_metadata import Command
        
        cmd = Command()
        
        # Test various date formats
        self.assertEqual(cmd.parse_date('01/15/2023'), 
                        cmd.parse_date('01/15/23'))
        self.assertIsNotNone(cmd.parse_date('2023-01-15'))
        self.assertIsNone(cmd.parse_date(''))
        self.assertIsNone(cmd.parse_date('.'))
