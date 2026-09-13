from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

from gallery.models import ImageMetadata
from gallery.serializers import (
    ImageMetadataSerializer, 
    ImageMetadataListSerializer,
    ImageMetadataDetailSerializer,
    BulkUpdateSerializer,
    BulkImportSerializer
)


class ImageMetadataViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ImageMetadata model with CRUD operations,
    filtering, sorting, search, and bulk operations.
    """
    queryset = ImageMetadata.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_value_regex = '[^/]+'  # Allow dots in primary keys (e.g., IMG_001.JPG)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'medium', 'substrate', 'orientation', 'part_of_gallery', 
        'location', 'in_inventory', 'currently_shown'
    ]
    search_fields = [
        'id_title', 'website_title', 'keywords', 'invent_number',
        'medium', 'location', 'currently_shown', 'shown_in_past'
    ]
    ordering_fields = [
        'image_file_name', 'invent_number', 'date', 'id_title', 
        'medium', 'number_sold', 'sale_price', 'created_at'
    ]
    ordering = ['image_file_name']

    def get_serializer_class(self):
        """Return appropriate serializer based on action"""
        if self.action == 'list':
            return ImageMetadataListSerializer
        elif self.action == 'retrieve':
            return ImageMetadataDetailSerializer
        return ImageMetadataSerializer

    def get_queryset(self):
        """Return queryset (filtering handled by filter backends)"""
        return super().get_queryset()

    @action(detail=False, methods=['post'])
    def bulk_update(self, request):
        """
        Bulk update metadata for multiple images.
        POST /api/images/bulk_update/
        Body: {
            "image_file_names": ["IMG_001.JPG", "IMG_002.JPG"],
            "updates": {"medium": "watercolor", "location": "Gallery A"}
        }
        """
        serializer = BulkUpdateSerializer(data=request.data)
        if serializer.is_valid():
            image_file_names = serializer.validated_data['image_file_names']
            updates = serializer.validated_data['updates']
            
            # Filter valid fields
            valid_fields = [f.name for f in ImageMetadata._meta.get_fields()]
            updates = {k: v for k, v in updates.items() if k in valid_fields}
            
            # Perform bulk update
            updated_count = ImageMetadata.objects.filter(
                image_file_name__in=image_file_names
            ).update(**updates)
            
            return Response({
                'message': f'Successfully updated {updated_count} records',
                'updated_count': updated_count
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def bulk_import(self, request):
        """
        Bulk import metadata from CSV or Excel file.
        POST /api/images/bulk_import/
        Body: {
            "file": <file>,
            "clear_existing": false
        }
        """
        serializer = BulkImportSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            clear_existing = serializer.validated_data.get('clear_existing', False)
            
            try:
                # Clear existing data if requested
                if clear_existing:
                    ImageMetadata.objects.all().delete()
                
                # Read file based on extension
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                elif file.name.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(file)
                else:
                    return Response(
                        {'error': 'Unsupported file format. Use CSV or Excel.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Process and import data
                imported_count = 0
                errors = []
                
                for index, row in df.iterrows():
                    try:
                        # Create metadata dict
                        metadata_dict = {}
                        for column in df.columns:
                            # Map column names to model fields
                            field_name = column.lower().replace(' ', '_').replace('-', '_')
                            # Clean up field name
                            field_name = ''.join(c for c in field_name if c.isalnum() or c == '_')
                            
                            if hasattr(ImageMetadata, field_name):
                                value = row[column]
                                if pd.notna(value):
                                    metadata_dict[field_name] = value
                        
                        # Ensure image_file_name is present
                        if 'image_file_name' not in metadata_dict:
                            errors.append(f'Row {index}: Missing image_file_name')
                            continue
                        
                        # Create or update record
                        ImageMetadata.objects.update_or_create(
                            image_file_name=metadata_dict['image_file_name'],
                            defaults=metadata_dict
                        )
                        imported_count += 1
                        
                    except Exception as e:
                        errors.append(f'Row {index}: {str(e)}')
                
                return Response({
                    'message': f'Successfully imported {imported_count} records',
                    'imported_count': imported_count,
                    'errors': errors[:10]  # Limit errors to first 10
                }, status=status.HTTP_200_OK)
                
            except Exception as e:
                return Response(
                    {'error': f'Import failed: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        """
        Export metadata to CSV format.
        GET /api/images/export_csv/
        """
        queryset = self.get_queryset()
        
        # Convert to DataFrame
        data = list(queryset.values())
        df = pd.DataFrame(data)
        
        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="image_metadata.csv"'
        
        df.to_csv(response, index=False)
        return response

    @action(detail=False, methods=['get'])
    def export_excel(self, request):
        """
        Export metadata to Excel format.
        GET /api/images/export_excel/
        """
        queryset = self.get_queryset()
        
        # Convert to DataFrame
        data = list(queryset.values())
        df = pd.DataFrame(data)
        
        # Excel does not support timezone-aware datetimes; convert to naive
        for col in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[col]):
                df[col] = df[col].dt.tz_localize(None)
            else:
                df[col] = df[col].apply(
                    lambda v: v.replace(tzinfo=None)
                    if hasattr(v, 'tzinfo') and v.tzinfo is not None else v
                )
        
        # Create Excel response
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="image_metadata.xlsx"'
        
        with BytesIO() as buffer:
            df.to_excel(buffer, index=False, engine='openpyxl')
            response.write(buffer.getvalue())
        
        return response

    @action(detail=False, methods=['get'])
    def export_pdf(self, request):
        """
        Export metadata to PDF format.
        GET /api/images/export_pdf/
        """
        queryset = self.get_queryset()
        
        # Create PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="image_metadata.pdf"'
        
        # Create PDF document
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        
        # Add title
        styles = getSampleStyleSheet()
        title = Paragraph("Image Metadata Report", styles['Title'])
        elements.append(title)
        
        # Create table data
        data = [['Image File', 'Title', 'Medium', 'Inventory #', 'Location']]
        for item in queryset[:50]:  # Limit to 50 records for PDF
            data.append([
                item.image_file_name,
                item.id_title or 'N/A',
                item.medium or 'N/A',
                item.invent_number or 'N/A',
                item.location or 'N/A'
            ])
        
        # Create table
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        doc.build(elements)
        
        response.write(buffer.getvalue())
        return response
