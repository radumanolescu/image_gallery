import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import Collapse from '@mui/material/Collapse'
import FormControl from '@mui/material/FormControl'
import InputLabel from '@mui/material/InputLabel'
import MenuItem from '@mui/material/MenuItem'
import Select from '@mui/material/Select'
import { useState } from 'react'
import ExpandMoreIcon from '@mui/icons-material/ExpandMore'
import ExpandLessIcon from '@mui/icons-material/ExpandLess'

export interface FilterValues {
  medium: string
  location: string
  part_of_gallery: string
  orientation: string
  substrate: string
  in_inventory: string
  currently_shown: string
}

const EMPTY_FILTERS: FilterValues = {
  medium: '',
  location: '',
  part_of_gallery: '',
  orientation: '',
  substrate: '',
  in_inventory: '',
  currently_shown: '',
}

const FILTER_DEFS: { key: keyof FilterValues; label: string }[] = [
  { key: 'medium', label: 'Medium' },
  { key: 'location', label: 'Location' },
  { key: 'part_of_gallery', label: 'Part of gallery' },
  { key: 'orientation', label: 'Orientation' },
  { key: 'substrate', label: 'Substrate' },
  { key: 'in_inventory', label: 'In inventory' },
  { key: 'currently_shown', label: 'Currently shown' },
]

interface FilterPanelProps {
  values: FilterValues
  options: Record<keyof FilterValues, string[]>
  onChange: (values: FilterValues) => void
}

export default function FilterPanel({
  values,
  options,
  onChange,
}: FilterPanelProps) {
  const [expanded, setExpanded] = useState(false)
  const activeCount = Object.values(values).filter(Boolean).length

  const update = (key: keyof FilterValues, value: string) =>
    onChange({ ...values, [key]: value })

  return (
    <Box>
      <Button
        size="small"
        onClick={() => setExpanded((v) => !v)}
        endIcon={expanded ? <ExpandLessIcon /> : <ExpandMoreIcon />}
      >
        Filters{activeCount > 0 ? ` (${activeCount})` : ''}
      </Button>
      {activeCount > 0 && (
        <Button size="small" onClick={() => onChange(EMPTY_FILTERS)}>
          Clear all
        </Button>
      )}
      <Collapse in={expanded}>
        <Box
          sx={{
            display: 'flex',
            gap: 2,
            flexWrap: 'wrap',
            mt: 1,
          }}
        >
          {FILTER_DEFS.map(({ key, label }) => (
            <FormControl key={key} size="small" sx={{ minWidth: 160 }}>
              <InputLabel>{label}</InputLabel>
              <Select
                value={values[key]}
                label={label}
                onChange={(e) => update(key, e.target.value)}
              >
                <MenuItem value="">
                  <em>All</em>
                </MenuItem>
                {options[key].map((opt) => (
                  <MenuItem key={opt} value={opt}>
                    {opt}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          ))}
        </Box>
      </Collapse>
    </Box>
  )
}

export { EMPTY_FILTERS }
