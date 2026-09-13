import { useRef, useState } from 'react'
import Alert from '@mui/material/Alert'
import Button from '@mui/material/Button'
import Checkbox from '@mui/material/Checkbox'
import Dialog from '@mui/material/Dialog'
import DialogActions from '@mui/material/DialogActions'
import DialogContent from '@mui/material/DialogContent'
import DialogTitle from '@mui/material/DialogTitle'
import FormControlLabel from '@mui/material/FormControlLabel'
import Typography from '@mui/material/Typography'
import { bulkImport } from '../api/images'
import type { BulkImportResponse } from '../api/types'

interface ImportDialogProps {
  open: boolean
  onClose: (imported: boolean) => void
}

export default function ImportDialog({ open, onClose }: ImportDialogProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [file, setFile] = useState<File | null>(null)
  const [clearExisting, setClearExisting] = useState(false)
  const [busy, setBusy] = useState(false)
  const [result, setResult] = useState<BulkImportResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const doImport = async () => {
    if (!file) return
    setBusy(true)
    setError(null)
    setResult(null)
    try {
      const res = await bulkImport(file, clearExisting)
      setResult(res)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Import failed')
    } finally {
      setBusy(false)
    }
  }

  const close = () => {
    const done = result !== null && result.errors.length === 0
    onClose(done)
    setFile(null)
    setResult(null)
    setError(null)
  }

  return (
    <Dialog open={open} onClose={close} maxWidth="sm" fullWidth>
      <DialogTitle>Import Metadata</DialogTitle>
      <DialogContent dividers>
        <Typography variant="body2" sx={{ mb: 2 }}>
          Upload a CSV or Excel file. Column names are mapped to metadata fields
          (e.g. <code>Image File Name</code> → <code>image_file_name</code>).
        </Typography>
        <input
          ref={inputRef}
          type="file"
          accept=".csv,.xlsx,.xls"
          style={{ display: 'none' }}
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        <Button variant="outlined" onClick={() => inputRef.current?.click()}>
          {file ? file.name : 'Choose file'}
        </Button>
        <FormControlLabel
          sx={{ display: 'block', mt: 1 }}
          control={
            <Checkbox
              checked={clearExisting}
              onChange={(e) => setClearExisting(e.target.checked)}
            />
          }
          label="Clear existing metadata before import"
        />
        {result && (
          <Alert
            severity={result.errors.length ? 'warning' : 'success'}
            sx={{ mt: 2 }}
          >
            {result.message}
            {result.errors.length > 0 && (
              <ul style={{ margin: '8px 0 0' }}>
                {result.errors.map((err, i) => (
                  <li key={i}>{err}</li>
                ))}
              </ul>
            )}
          </Alert>
        )}
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={close}>Close</Button>
        <Button
          variant="contained"
          onClick={doImport}
          disabled={!file || busy}
        >
          {busy ? 'Importing…' : 'Import'}
        </Button>
      </DialogActions>
    </Dialog>
  )
}
