from django.db import models


class ImageMetadata(models.Model):
    """
    Model for storing image metadata.
    Primary key is the image file name.
    """
    image_file_name = models.CharField(
        max_length=255,
        primary_key=True,
        help_text="Image file name (e.g., IMG_7493.JPG)"
    )

    # Metadata fields from the template, converted to snake_case
    invent_number = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Inventory number"
    )
    invent_img = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Inventory image number"
    )
    high_res_image = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="High resolution image reference"
    )
    date = models.DateField(
        blank=True,
        null=True,
        help_text="Date associated with the image"
    )
    id_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="ID title"
    )
    website_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Website title"
    )
    part_of_gallery = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Part of a gallery"
    )
    medium = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Art medium"
    )
    substrate = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Substrate material"
    )
    dimensions_hxwxd = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Dimensions (Height x Width x Depth)"
    )
    orientation = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Image orientation"
    )
    edition = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Edition information"
    )
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Location"
    )
    in_inventory = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="In inventory status"
    )
    number_sold = models.IntegerField(
        blank=True,
        null=True,
        help_text="Number of items sold"
    )
    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Sale price"
    )
    cost_of_goods = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Cost of goods"
    )
    current_inventory = models.IntegerField(
        blank=True,
        null=True,
        help_text="Current inventory count"
    )
    goods_sold = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Goods sold value"
    )
    currently_shown = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Currently shown location"
    )
    shown_in_past = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Previously shown locations"
    )
    keywords = models.TextField(
        blank=True,
        null=True,
        help_text="Keywords for search"
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Record creation timestamp"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Record last update timestamp"
    )

    class Meta:
        db_table = 'image_metadata'
        verbose_name = 'Image Metadata'
        verbose_name_plural = 'Image Metadata'
        ordering = ['image_file_name']

    def __str__(self):
        return f"{self.image_file_name} - {self.id_title or 'Untitled'}"
