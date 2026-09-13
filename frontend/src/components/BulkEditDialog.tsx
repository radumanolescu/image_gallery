import { useState } from 'react'
import Alert from '@mui/material/Alert'
import Button from '@mui/material/Button'
import Dialog from '@mui/material/Dialog'
import DialogActions from '@mui/material/DialogActions'
import DialogContent from '@mui/material/DialogContent'
import DialogTitle from '@mui/material/DialogTitle'
import FormControl from '@mui/material/FormControl'
import InputLabel from '@mui/material/InputLabel'
import ListItemText from '@mui/material/ListItemText'
import MenuItem from '@mui/material/MenuItem'
import Select from '@mui/material/Select'
import TextField from '@mui/material/TextField'
import Typography from '@mui/material/Typography'
import type { ImageMetadata } from '../api/types'
import { bulkUpdate } from '../api/images'

// Fields that make sense to update in bulk.
const BULK_FIELDS: { key: keyof ImageMetadata; label: string }[] = [
  { key: 'medium', label: 'Medium' },
  { key: 'substrate', label: 'Substrate' },
  { key: 'orientation', label: 'Orientation' },
  { key: 'part_of_gallery', label: 'Part of a Gallery' },
  { key: 'location', label: 'Location' },
  { key: 'in_inventory', label: 'In Inventory' },
  { key: 'currently_shown', label: 'Currently Shown' },
  { key: 'shown_in_past', label: 'Shown in Past' },
  { key: 'edition', label: 'Edition' },
]

interface BulkEditDialogProps {
  fileNames: string[]
  open: boolean
  onClose: (updated: boolean) => void
}

export default function BulkEditDialog({
  fileNames,
  open,
  onClose,
}: BulkEditDialogProps) {
  const [field, setField] = useState<keyof ImageMetadata>('medium')
  const [value, setValue] = useState('')
  const [busy, setBusy] = useState(false)
  const [result, setResult] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)

  const apply = async () => {
    setBusy(true)
    setError(null)
    setResult(null)
    try {
      const res = await bulkUpdate({
        image_file_names: fileNames,
        updates: { [field]: value },
      })
      setResult(res.message)
      setTimeout(() => onClose(true), 1200)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Bulk update failed')
    } finally {
      setBusy(false)
    }
  }

  return (
    <Dialog open={open} onClose={() => onClose(false)} maxWidth="sm" fullWidth>
      <DialogTitle>Bulk Edit — {fileNames.length} images</DialogTitle>
      <DialogContent dividers>
        <Typography variant="body2" sx={{ mb: 2 }}>
          Choose a field and a new value to apply to all selected images.
        </Typography>
        <FormControl fullWidth size="small" sx={{ mb: 2 }}>
          <InputLabel>Field</InputLabel>
          <Select
            value={field}
            label="Field"
            onChange={(e) => setField(e.target.value as keyof ImageMetadata)}
          >
            {BULK_FIELDS.map((f) => (
              <MenuItem key={f.key} value={f.key}>
                <ListItemText primary={f.label} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <TextField
          fullWidth
          size="small"
          label="New value"
          value={value}
          onChange={(e) => setValue(e.target.value)}
        />
        <Typography
          variant="caption"
          color="text.secondary"
          sx={{ display: 'block', mt: 2, wordBreak: 'break-all' }}
        >
          {fileNames.join(', ')}
        </Typography>
        {result && (
          <Alert severity="success" sx={{ mt: 2 }}>
            {result}
          </Alert>
        )}
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={() => onClose(false)}>Cancel</Button>
        <Button
          variant="contained"
          onClick={apply}
          disabled={busy || fileNames.length === 0}
        >
          {busy ? 'Applying…' : 'Apply to selected'}
        </Button>
      </DialogActions>
    </Dialog>
  )
}
