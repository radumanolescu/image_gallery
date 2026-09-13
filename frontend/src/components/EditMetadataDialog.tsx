import { useEffect, useState } from 'react'
import Button from '@mui/material/Button'
import Dialog from '@mui/material/Dialog'
import DialogActions from '@mui/material/DialogActions'
import DialogContent from '@mui/material/DialogContent'
import DialogTitle from '@mui/material/DialogTitle'
import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import Grid from '@mui/material/Grid'
import Box from '@mui/material/Box'
import CircularProgress from '@mui/material/CircularProgress'
import type { ImageMetadata } from '../api/types'
import { getImage, updateImage } from '../api/images'
import { imageUrl } from '../api/client'

// Editable fields grouped by section, matching the model.
const FIELD_GROUPS: {
  title: string
  fields: { key: keyof ImageMetadata; label: string; type?: string }[]
}[] = [
  {
    title: 'Identification',
    fields: [
      { key: 'invent_number', label: 'Invent. Number' },
      { key: 'invent_img', label: 'Invent. IMG-' },
      { key: 'high_res_image', label: 'High Res Image' },
      { key: 'date', label: 'Date', type: 'date' },
      { key: 'id_title', label: 'ID Title' },
      { key: 'website_title', label: 'Website Title' },
    ],
  },
  {
    title: 'Artwork',
    fields: [
      { key: 'part_of_gallery', label: 'Part of a Gallery' },
      { key: 'medium', label: 'Medium' },
      { key: 'substrate', label: 'Substrate' },
      { key: 'dimensions_hxwxd', label: 'Dimensions HxWxD' },
      { key: 'orientation', label: 'Orientation' },
      { key: 'edition', label: 'Edition' },
      { key: 'location', label: 'Location' },
    ],
  },
  {
    title: 'Inventory & Sales',
    fields: [
      { key: 'in_inventory', label: 'In Inventory' },
      { key: 'number_sold', label: 'Number Sold', type: 'number' },
      { key: 'sale_price', label: 'Sale Price', type: 'number' },
      { key: 'cost_of_goods', label: 'Cost of Goods', type: 'number' },
      { key: 'current_inventory', label: 'Current Inventory', type: 'number' },
      { key: 'goods_sold', label: 'Goods Sold', type: 'number' },
    ],
  },
  {
    title: 'Exhibition & Keywords',
    fields: [
      { key: 'currently_shown', label: 'Currently Shown' },
      { key: 'shown_in_past', label: 'Shown in Past' },
      { key: 'keywords', label: 'Keywords' },
    ],
  },
]

interface EditMetadataDialogProps {
  fileName: string | null
  open: boolean
  onClose: (saved: boolean) => void
}

export default function EditMetadataDialog({
  fileName,
  open,
  onClose,
}: EditMetadataDialogProps) {
  const [form, setForm] = useState<Partial<ImageMetadata>>({})
  const [loading, setLoading] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (open && fileName) {
      setLoading(true)
      setError(null)
      getImage(fileName)
        .then(setForm)
        .catch((e) => setError(e.message))
        .finally(() => setLoading(false))
    }
  }, [open, fileName])

  const setField = (key: keyof ImageMetadata, value: string) =>
    setForm((f) => ({ ...f, [key]: value === '' ? null : value }))

  const handleSave = async () => {
    if (!fileName) return
    setSaving(true)
    setError(null)
    try {
      // Strip read-only fields before sending.
      const { created_at: _c, updated_at: _u, ...payload } = form
      await updateImage(fileName, payload)
      onClose(true)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Save failed')
    } finally {
      setSaving(false)
    }
  }

  return (
    <Dialog open={open} onClose={() => onClose(false)} maxWidth="md" fullWidth>
      <DialogTitle>Edit Metadata — {fileName}</DialogTitle>
      <DialogContent dividers>
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            {fileName && (
              <Box sx={{ mb: 2, textAlign: 'center' }}>
                <img
                  src={imageUrl(fileName)}
                  alt={fileName}
                  style={{ maxHeight: 200, maxWidth: '100%' }}
                />
              </Box>
            )}
            {FIELD_GROUPS.map((group) => (
              <Box key={group.title} sx={{ mb: 2 }}>
                <Typography variant="overline" color="text.secondary">
                  {group.title}
                </Typography>
                <Grid container spacing={2}>
                  {group.fields.map(({ key, label, type }) => (
                    <Grid key={key} size={{ xs: 12, sm: 6 }}>
                      <TextField
                        fullWidth
                        size="small"
                        label={label}
                        type={type ?? 'text'}
                        value={(form[key] as string | number | null) ?? ''}
                        onChange={(e) => setField(key, e.target.value)}
                        slotProps={{
                          inputLabel:
                            type === 'date' ? { shrink: true } : undefined,
                        }}
                        multiline={key === 'keywords'}
                      />
                    </Grid>
                  ))}
                </Grid>
              </Box>
            ))}
          </>
        )}
        {error && (
          <Typography color="error" variant="body2">
            {error}
          </Typography>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={() => onClose(false)}>Cancel</Button>
        <Button
          variant="contained"
          onClick={handleSave}
          disabled={saving || loading}
        >
          {saving ? 'Saving…' : 'Save'}
        </Button>
      </DialogActions>
    </Dialog>
  )
}
