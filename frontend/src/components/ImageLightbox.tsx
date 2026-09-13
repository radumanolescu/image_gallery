import Lightbox from 'yet-another-react-lightbox'
import Zoom from 'yet-another-react-lightbox/plugins/zoom'
import 'yet-another-react-lightbox/styles.css'
import Box from '@mui/material/Box'
import Typography from '@mui/material/Typography'
import Chip from '@mui/material/Chip'
import { imageUrl } from '../api/client'
import type { ImageMetadata } from '../api/types'

interface ImageLightboxProps {
  images: ImageMetadata[]
  index: number
  onClose: () => void
}

export default function ImageLightbox({
  images,
  index,
  onClose,
}: ImageLightboxProps) {
  const slides = images.map((img) => ({
    src: imageUrl(img.image_file_name),
    title: img.id_title ?? img.image_file_name,
    description: [img.medium, img.invent_number ? `#${img.invent_number}` : null]
      .filter(Boolean)
      .join(' · '),
  }))

  const current = index >= 0 && index < images.length ? images[index] : null

  return (
    <>
      <Lightbox
        open={index >= 0}
        close={onClose}
        index={index >= 0 ? index : 0}
        slides={slides}
        plugins={[Zoom]}
      />
      {/* Metadata strip shown while the lightbox is open */}
      {index >= 0 && current && (
        <Box
          sx={{
            position: 'fixed',
            bottom: 0,
            left: 0,
            right: 0,
            zIndex: 1400,
            bgcolor: 'rgba(0,0,0,0.75)',
            color: 'white',
            p: 1.5,
            display: 'flex',
            gap: 1,
            flexWrap: 'wrap',
            alignItems: 'center',
          }}
        >
          <Typography variant="subtitle2">
            {current.id_title || current.image_file_name}
          </Typography>
          {current.medium && (
            <Chip label={current.medium} size="small" sx={{ color: 'white' }} />
          )}
          {current.invent_number && (
            <Chip
              label={`#${current.invent_number}`}
              size="small"
              variant="outlined"
              sx={{ color: 'white' }}
            />
          )}
          {current.dimensions_hxwxd && (
            <Typography variant="caption">{current.dimensions_hxwxd}</Typography>
          )}
        </Box>
      )}
    </>
  )
}
