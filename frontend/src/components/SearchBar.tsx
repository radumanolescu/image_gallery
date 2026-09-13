import { useEffect, useState } from 'react'
import Box from '@mui/material/Box'
import FormControl from '@mui/material/FormControl'
import InputLabel from '@mui/material/InputLabel'
import MenuItem from '@mui/material/MenuItem'
import Select from '@mui/material/Select'
import TextField from '@mui/material/TextField'
import InputAdornment from '@mui/material/InputAdornment'
import IconButton from '@mui/material/IconButton'
import SearchIcon from '@mui/icons-material/Search'
import ClearIcon from '@mui/icons-material/Clear'

interface SearchBarProps {
  search: string
  ordering: string
  onSearchChange: (value: string) => void
  onOrderingChange: (value: string) => void
}

const ORDERING_OPTIONS = [
  { value: 'image_file_name', label: 'File name' },
  { value: 'invent_number', label: 'Inventory #' },
  { value: 'date', label: 'Date' },
  { value: 'id_title', label: 'Title' },
  { value: 'medium', label: 'Medium' },
  { value: 'number_sold', label: 'Number sold' },
  { value: 'sale_price', label: 'Sale price' },
  { value: 'created_at', label: 'Created' },
]

export default function SearchBar({
  search,
  ordering,
  onSearchChange,
  onOrderingChange,
}: SearchBarProps) {
  const [input, setInput] = useState(search)

  // Debounce the search input before pushing it upstream.
  useEffect(() => {
    const t = setTimeout(() => {
      if (input !== search) onSearchChange(input)
    }, 400)
    return () => clearTimeout(t)
  }, [input, search, onSearchChange])

  const descending = ordering.startsWith('-')
  const orderField = descending ? ordering.slice(1) : ordering

  return (
    <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', alignItems: 'center' }}>
      <TextField
        label="Search"
        size="small"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        sx={{ minWidth: 280, flexGrow: 1 }}
        slotProps={{
          input: {
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
            endAdornment: input ? (
              <InputAdornment position="end">
                <IconButton
                  size="small"
                  aria-label="clear search"
                  onClick={() => {
                    setInput('')
                    onSearchChange('')
                  }}
                >
                  <ClearIcon />
                </IconButton>
              </InputAdornment>
            ) : undefined,
          },
        }}
      />
      <FormControl size="small" sx={{ minWidth: 160 }}>
        <InputLabel>Sort by</InputLabel>
        <Select
          value={orderField}
          label="Sort by"
          onChange={(e) =>
            onOrderingChange(descending ? `-${e.target.value}` : e.target.value)
          }
        >
          {ORDERING_OPTIONS.map((o) => (
            <MenuItem key={o.value} value={o.value}>
              {o.label}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
      <FormControl size="small" sx={{ minWidth: 120 }}>
        <InputLabel>Direction</InputLabel>
        <Select
          value={descending ? 'desc' : 'asc'}
          label="Direction"
          onChange={(e) =>
            onOrderingChange(
              e.target.value === 'desc' ? `-${orderField}` : orderField
            )
          }
        >
          <MenuItem value="asc">Ascending</MenuItem>
          <MenuItem value="desc">Descending</MenuItem>
        </Select>
      </FormControl>
    </Box>
  )
}
