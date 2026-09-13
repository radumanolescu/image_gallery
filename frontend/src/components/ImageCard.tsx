import Card from '@mui/material/Card'
import CardActionArea from '@mui/material/CardActionArea'
import CardContent from '@mui/material/CardContent'
import CardMedia from '@mui/material/CardMedia'
import Checkbox from '@mui/material/Checkbox'
import Chip from '@mui/material/Chip'
import IconButton from '@mui/material/IconButton'
import Typography from '@mui/material/Typography'
import Box from '@mui/material/Box'
import EditIcon from '@mui/icons-material/Edit'
import BrokenImageIcon from '@mui/icons-material/BrokenImage'
import { useState } from 'react'
import type { ImageMetadata } from '../api/types'
import { imageUrl } from '../api/client'

interface ImageCardProps {
  image: ImageMetadata
  selected: boolean
  selectable: boolean
  onSelect: (fileName: string, selected: boolean) => void
  onPreview: (image: ImageMetadata) => void
  onEdit: (image: ImageMetadata) => void
}

export default function ImageCard({
  image,
  selected,
  selectable,
  onSelect,
  onPreview,
  onEdit,
}: ImageCardProps) {
  const [imgError, setImgError] = useState(false)

  return (
    <Card sx={{ position: 'relative' }}>
      {selectable && (
        <Checkbox
          checked={selected}
          onChange={(e) => onSelect(image.image_file_name, e.target.checked)}
          sx={{
            position: 'absolute',
            top: 4,
            left: 4,
            zIndex: 2,
            bgcolor: 'rgba(255,255,255,0.8)',
            borderRadius: 1,
            p: 0.5,
          }}
        />
      )}
      <IconButton
        size="small"
        aria-label={`edit ${image.image_file_name}`}
        onClick={() => onEdit(image)}
        sx={{
          position: 'absolute',
          top: 4,
          right: 4,
          zIndex: 2,
          bgcolor: 'rgba(255,255,255,0.8)',
        }}
      >
        <EditIcon fontSize="small" />
      </IconButton>
      <CardActionArea onClick={() => onPreview(image)}>
        {imgError ? (
          <Box
            sx={{
              height: 180,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              bgcolor: 'grey.200',
            }}
          >
            <BrokenImageIcon fontSize="large" color="disabled" />
          </Box>
        ) : (
          <CardMedia
            component="img"
            height="180"
            image={imageUrl(image.image_file_name)}
            alt={image.id_title ?? image.image_file_name}
            loading="lazy"
            onError={() => setImgError(true)}
            sx={{ objectFit: 'cover' }}
          />
        )}
        <CardContent sx={{ flexGrow: 1 }}>
          <Typography variant="subtitle2" noWrap title={image.id_title ?? ''}>
            {image.id_title || image.image_file_name}
          </Typography>
          <Typography
            variant="caption"
            color="text.secondary"
            sx={{ display: 'block' }}
          >
            {image.image_file_name}
          </Typography>
          <Box sx={{ mt: 1, display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
            {image.medium && (
              <Chip label={image.medium} size="small" variant="outlined" />
            )}
            {image.invent_number && (
              <Chip
                label={`#${image.invent_number}`}
                size="small"
                variant="outlined"
              />
            )}
          </Box>
        </CardContent>
      </CardActionArea>
    </Card>
  )
}
