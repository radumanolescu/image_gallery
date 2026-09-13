from django.contrib import admin
from gallery.models import ImageMetadata

# Customize the admin interface
admin.site.site_header = "Image Gallery Admin"
admin.site.site_title = "Image Gallery Admin Portal"
admin.site.index_title = "Welcome to Image Gallery Administration"


@admin.register(ImageMetadata)
class ImageMetadataAdmin(admin.ModelAdmin):
    """Admin interface for ImageMetadata model"""
    list_display = [
        'image_file_name', 'id_title', 'medium', 'invent_number', 
        'number_sold', 'sale_price', 'created_at', 'updated_at'
    ]
    list_filter = ['medium', 'orientation', 'part_of_gallery', 'location']
    search_fields = ['image_file_name', 'id_title', 'website_title', 'keywords']
    readonly_fields = ['created_at', 'updated_at']
    list_per_page = 50
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('image_file_name', 'id_title', 'website_title', 'keywords')
        }),
        ('Inventory Details', {
            'fields': ('invent_number', 'invent_img', 'high_res_image', 'date')
        }),
        ('Artwork Details', {
            'fields': ('medium', 'substrate', 'dimensions_hxwxd', 'orientation', 
                      'edition', 'part_of_gallery', 'location')
        }),
        ('Sales Information', {
            'fields': ('in_inventory', 'number_sold', 'sale_price', 
                      'cost_of_goods', 'current_inventory', 'goods_sold')
        }),
        ('Exhibition History', {
            'fields': ('currently_shown', 'shown_in_past')
        }),
        ('System Information', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
