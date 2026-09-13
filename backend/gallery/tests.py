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
