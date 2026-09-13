from rest_framework import serializers
from gallery.models import ImageMetadata


class ImageMetadataSerializer(serializers.ModelSerializer):
    """Serializer for ImageMetadata model"""
    
    class Meta:
        model = ImageMetadata
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ImageMetadataListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    
    class Meta:
        model = ImageMetadata
        fields = [
            'image_file_name', 'id_title', 'website_title', 'medium', 
            'invent_number', 'part_of_gallery', 'location', 'currently_shown'
        ]


class ImageMetadataDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single image views"""
    
    class Meta:
        model = ImageMetadata
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class BulkUpdateSerializer(serializers.Serializer):
    """Serializer for bulk update operations"""
    image_file_names = serializers.ListField(
        child=serializers.CharField(),
        allow_empty=False,
        help_text="List of image file names to update"
    )
    updates = serializers.DictField(
        help_text="Dictionary of field names and values to update"
    )


class BulkImportSerializer(serializers.Serializer):
    """Serializer for bulk import operations"""
    file = serializers.FileField(
        help_text="CSV or Excel file containing metadata to import"
    )
    clear_existing = serializers.BooleanField(
        default=False,
        required=False,
        help_text="Clear existing metadata before import"
    )