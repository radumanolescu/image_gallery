import Grid from '@mui/material/Grid'
import type { ImageMetadata } from '../api/types'
import ImageCard from './ImageCard'

interface ImageGridProps {
  images: ImageMetadata[]
  selected: Set<string>
  selectable: boolean
  onSelect: (fileName: string, selected: boolean) => void
  onPreview: (image: ImageMetadata) => void
  onEdit: (image: ImageMetadata) => void
}

export default function ImageGrid({
  images,
  selected,
  selectable,
  onSelect,
  onPreview,
  onEdit,
}: ImageGridProps) {
  return (
    <Grid container spacing={2}>
      {images.map((img) => (
        <Grid key={img.image_file_name} size={{ xs: 12, sm: 6, md: 4, lg: 3 }}>
          <ImageCard
            image={img}
            selected={selected.has(img.image_file_name)}
            selectable={selectable}
            onSelect={onSelect}
            onPreview={onPreview}
            onEdit={onEdit}
          />
        </Grid>
      ))}
    </Grid>
  )
}
