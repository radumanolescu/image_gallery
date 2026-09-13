# Image Gallery - Agent Instructions

## Project Overview
A Flask-based image gallery web application that runs locally and allows viewing, filtering, sorting, and editing image metadata. Images are stored with corresponding text files containing metadata fields.

## Technology Stack
- **Framework**: Flask
- **Data Processing**: pandas
- **Storage**: Text files (.txt) for metadata, static files for images
- **Language**: Python 3

## Prerequisites
- Python 3.x
- Flask installed (`pip install flask`)
- pandas installed (`pip install pandas`)
- Host configuration file at `C:/sw/conf/host_conf.json` with structure:
  ```json
  {
    "image_gallery": {
      "root_dir": "path/to/image_gallery"
    }
  }
  ```

## Running the Application

1. **Activate the conda environment** (if using conda):
   ```bash
   conda activate web
   ```

2. **Navigate to the project directory**:
   ```bash
   cd C:\Users\Radu\-\projects\Python\image_gallery
   ```

3. **Start the Flask development server**:
   ```bash
   flask run
   ```

4. **Access the application**:
   Open a browser and navigate to `http://localhost:5000/index`

## Project Structure

```
image_gallery/
├── app.py                 # Flask application with routes
├── image_list.py          # High-level methods for web app routes
├── txt_db.py              # Database-like operations using text files and pandas
├── create_thumbnails.py   # Utility for creating image thumbnails
├── fix_inv_num_img.py     # Utility for fixing inventory numbers
├── MetadataTemplate.txt    # Template defining metadata field names
├── static/
│   ├── images/            # Directory for image files (.JPG)
│   │   └── *.txt          # Metadata files (one per image)
│   └── index.css          # Stylesheet
├── templates/
│   ├── index.html         # Main gallery view with filtering/sorting
│   └── edit_metadata.html # Metadata editing interface
└── AGENTS.md              # This file
```

## Key Components

### app.py
Flask application with three main routes:
- `/index` - Main gallery view with filtering and sorting capabilities
- `/edit_metadata` - Form for editing metadata for a specific image
- `/save_metadata` - Saves edited metadata back to text file

### image_list.py
High-level functions called by Flask routes:
- `read_headings()` - Reads metadata template file
- `metadata_headings()` - Reads field names from a metadata file
- `metadata_indexed_values()` - Reads values from a metadata file
- `all_meta()` - Loads all metadata files
- `selected_meta()` - Filters and sorts metadata based on user input
- `save_meta()` - Saves metadata to text file

### txt_db.py
Database-like operations using pandas:
- `load_metadata()` - Loads all metadata into a pandas DataFrame
- `select()` - Filters DataFrame based on criteria
- `order()` - Sorts DataFrame based on criteria
- `ranges()` - Computes unique values for filter dropdowns
- `metadata_dict()` - Converts metadata file to dictionary
- `apply_types()` - Applies proper data types (int, float, date) to metadata

### Metadata Storage
- Each image has a corresponding `.txt` file with the same base name
- Metadata files use tab-separated format: `field_name\tvalue`
- `MetadataTemplate.txt` defines the field names and order

## Metadata Fields
Defined in `txt_db.py`:
- Image file
- Invent. Number
- Invent. IMG-
- Hig Res Image
- Date
- ID Title
- Website Title
- Part of a Gallery
- Medium
- Substrate
- Dimensions HxWxD
- Orientation
- Edition
- Location
- in Inventory
- Number Sold
- Sale Price
- Cost of Goods
- Current Inventory
- Goods Sold
- Currently Shown
- Shown in Past
- Keywords

## Development Notes

### Adding New Metadata Fields
1. Add the field to `MetadataTemplate.txt`
2. Update the `image_cols` dictionary in `txt_db.py` with appropriate data type
3. Add to appropriate column name lists (`int_col_names`, `float_col_names`, etc.) if needed
4. Add to `all_filter_col_names` or `all_sort_col_names` if it should be filterable/sortable

### File Naming Convention
- Images: `.JPG` extension
- Metadata files: `.txt` extension with same base name as image
- Example: `IMG_7493.JPG` → `IMG_7493.txt`

### Known Limitations
- Metadata refresh reloads entire DataFrame (could be optimized to refresh only changed file)
- Image file renaming is not supported (explicitly disabled per user request)
- No authentication or user management
- Development server only (not production-ready)

## Testing
No automated test suite is currently configured. Manual testing is performed by:
1. Starting the Flask server
2. Navigating to `/index` to view the gallery
3. Testing filter and sort functionality
4. Editing metadata for an image
5. Verifying changes are saved and persisted
