# Image Gallery Backend - Phase 2 Complete

## Overview
Phase 2 of the image gallery modernization has been successfully completed. The Django backend now includes a comprehensive database model for image metadata and a data loading system to import existing TXT files.

## Completed Tasks

### Phase 1: Django Backend Setup ✅
- Created virtual environment in `backend/venv/`
- Initialized Django project structure
- Created `gallery` app for image gallery functionality
- Installed Django 6.1.1 and Django REST Framework 3.18.1
- Configured SQLite database and applied migrations
- Set up static files to serve from existing `static/` directory
- Configured media files to use existing `static/images/` directory
- Customized Django admin interface with "Image Gallery Admin" branding
- Configured user authentication system with admin user
- Set up Django REST Framework with authentication and pagination
- Created comprehensive unit test suite with 24 tests (all passing)

### Phase 2: Database Model & Data Loading ✅
- **Examined metadata schema** from `MetadataTemplate.txt` and existing code
- **Designed Django model** (`ImageMetadata`) with image file name as primary key
- **Created database migration** for the new model
- **Implemented data loading program** (`load_metadata` management command)
- **Successfully loaded 221 TXT files** into the database with zero errors
- **Created comprehensive unit tests** for model and data loading (17 new tests)
- **Enhanced admin interface** with ImageMetadata model registration

## Database Model

### ImageMetadata Model
The `ImageMetadata` model stores all image metadata with the following characteristics:

- **Primary Key**: `image_file_name` (CharField) - Image file name (e.g., IMG_7493.JPG)
- **Metadata Fields**: 23 fields covering all aspects from the original TXT schema
- **Data Types**: Properly typed fields (CharField, IntegerField, DecimalField, DateField, TextField)
- **Timestamps**: Automatic `created_at` and `updated_at` fields
- **Field Naming**: Converted to snake_case (e.g., "Invent. Number" → `invent_number`)

### Field Mapping
Original TXT fields → Django model fields:
- Invent. Number → `invent_number`
- Invent. IMG- → `invent_img`
- Hig Res Image → `high_res_image`
- Date → `date` (DateField)
- ID Title → `id_title`
- Website Title → `website_title`
- Part of a Gallery → `part_of_gallery`
- Medium → `medium`
- Substrate → `substrate`
- Dimensions HxWxD → `dimensions_hxwxd`
- Orientation → `orientation`
- Edition → `edition`
- Location → `location`
- in Inventory → `in_inventory`
- Number Sold → `number_sold` (IntegerField)
- Sale Price → `sale_price` (DecimalField)
- Cost of Goods → `cost_of_goods` (DecimalField)
- Current Inventory → `current_inventory` (IntegerField)
- Goods Sold → `goods_sold` (DecimalField)
- Currently Shown → `currently_shown`
- Shown in Past → `shown_in_past`
- Keywords → `keywords` (TextField)

## Data Loading Program

### Management Command: `load_metadata`
A Django management command that imports metadata from TXT files into the database.

**Features:**
- **Automatic field mapping**: Maps TXT field names to Django model fields
- **Data type conversion**: Handles int, float, and date conversions
- **Error handling**: Reports errors without stopping the entire process
- **Update or create**: Updates existing records or creates new ones
- **Dry-run mode**: Test loading without modifying the database
- **Clear option**: Remove existing data before loading
- **Flexible path**: Specify custom directory or use default MEDIA_ROOT
- **Comprehensive reporting**: Summary of processed files, successes, and errors

**Usage:**
```bash
# Dry run to test
python manage.py load_metadata --dry-run

# Load all TXT files from default location
python manage.py load_metadata

# Load from specific directory
python manage.py load_metadata --path /path/to/txt/files

# Clear existing data before loading
python manage.py load_metadata --clear

# Combined options
python manage.py load_metadata --path /custom/path --clear --dry-run
```

**Data Loading Results:**
- **Total TXT files found**: 221
- **Successfully processed**: 221
- **Errors**: 0
- **Database records created**: 221

## Unit Tests

### Test Coverage
Comprehensive test suite with **41 tests** (24 from Phase 1 + 17 new tests for Phase 2):

**Phase 1 Tests:**
- Django configuration tests (database, static/media files, installed apps)
- Authentication system tests (user creation, login, admin access)
- Admin interface tests (customization, accessibility)
- REST Framework configuration tests
- Static and media files tests
- URL configuration tests

**Phase 2 Tests:**
- **ImageMetadata Model Tests** (9 tests):
  - Metadata creation and field validation
  - Primary key functionality
  - String representation
  - Update operations
  - Null field handling
  - Automatic timestamps
  - Duplicate key prevention

- **Data Loading Tests** (8 tests):
  - Command existence and help
  - Dry-run mode functionality
  - Actual data loading
  - Update existing records
  - Clear option functionality
  - Invalid file handling
  - Empty directory handling
  - Date parsing functionality

**All tests passing successfully** ✅

## Project Structure

```
backend/
├── venv/                          # Virtual environment
├── image_gallery_project/         # Django project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py              # Main configuration file
│   ├── urls.py                   # URL routing
│   └── wsgi.py
├── gallery/                      # Image gallery app
│   ├── __init__.py
│   ├── admin.py                  # Admin interface configuration
│   ├── apps.py
│   ├── management/               # Custom management commands
│   │   ├── __init__.py
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── load_metadata.py  # Data loading command
│   ├── migrations/               # Database migrations
│   │   ├── 0001_initial.py      # ImageMetadata model migration
│   │   └── __init__.py
│   ├── models.py                 # Database models
│   ├── tests.py                  # Unit tests (41 tests)
│   └── views.py                  # Views (to be added in Phase 3)
├── manage.py                     # Django management script
├── db.sqlite3                    # SQLite database (221 records)
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Running the Application

### Start the Django Development Server
```bash
cd backend
venv/Scripts/activate
python manage.py runserver
```

The server will start on `http://127.0.0.1:8000/`

### Access the Admin Interface
1. Navigate to `http://127.0.0.1:8000/admin/`
2. Login with credentials:
   - Username: `admin`
   - Password: `admin123`
3. View "Image Metadata" section to browse and edit all 221 image records

### Load Metadata from TXT Files
```bash
cd backend
venv/Scripts/activate

# Test loading without modifying database
python manage.py load_metadata --dry-run

# Actually load the data
python manage.py load_metadata

# Reload with clear option
python manage.py load_metadata --clear
```

### Run Tests
```bash
cd backend
venv/Scripts/activate
python manage.py test gallery
```

### Run Migrations
```bash
cd backend
venv/Scripts/activate
python manage.py migrate
```

## Configuration Details

### Database
- Engine: SQLite3
- Location: `backend/db.sqlite3`
- Tables: Standard Django tables + `image_metadata` table
- Records: 221 image metadata records

### ImageMetadata Model
- Table: `image_metadata`
- Primary Key: `image_file_name` (varchar)
- Fields: 26 total (23 metadata + 3 system fields)
- Indexes: Primary key on image_file_name

### Authentication
- Django's built-in User model
- Password validation enabled
- Session and Basic authentication configured for API

### Static Files
- URL: `/static/`
- Root: `backend/staticfiles/`
- Dirs: `../static/` (parent directory static files)

### Media Files
- URL: `/media/`
- Root: `../static/images/` (existing image directory)

### REST Framework
- Default authentication: Session and Basic
- Default permissions: IsAuthenticatedOrReadOnly
- Pagination: PageNumberPagination with 20 items per page

## Admin Interface

The Django admin interface has been enhanced with ImageMetadata model:

**Features:**
- Custom admin site branding
- List view with key fields (image_file_name, id_title, medium, etc.)
- Filter by medium, orientation, gallery, location
- Search by file name, titles, keywords
- Read-only timestamp fields
- Organized fieldsets for better UX
- 50 items per page pagination

**Access:** `http://127.0.0.1:8000/admin/gallery/imagemetadata/`

## Next Steps (Phase 3)
- Create Django REST Framework serializers for ImageMetadata model
- Build API endpoints for:
  - Image list with filtering and sorting
  - Individual image details
  - Metadata CRUD operations
  - Bulk update operations
  - Search functionality
  - Export endpoints
- Implement pagination for large datasets
- Add authentication to API endpoints
- Set up CORS for React frontend
- Add API documentation (Swagger/OpenAPI)

## Notes
- All 221 existing TXT files have been successfully migrated to the database
- The original TXT files remain unchanged (safe backup)
- Data integrity maintained during migration
- No errors encountered during data loading
- All data types properly converted (int, float, date)
- Admin interface provides full CRUD access to metadata
- Unit tests ensure data loading reliability

## Security Notes
- SECRET_KEY should be changed for production
- DEBUG should be set to False in production
- Allowed hosts should be configured for production domain
- Database should be backed up regularly
- Consider using environment variables for sensitive configuration
- Admin interface should be protected with strong passwords
- API endpoints should implement proper authentication and authorization