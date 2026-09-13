import { useCallback, useEffect, useMemo, useState } from 'react'
import Alert from '@mui/material/Alert'
import AppBar from '@mui/material/AppBar'
import Box from '@mui/material/Box'
import Button from '@mui/material/Button'
import CircularProgress from '@mui/material/CircularProgress'
import Container from '@mui/material/Container'
import Pagination from '@mui/material/Pagination'
import Toolbar from '@mui/material/Toolbar'
import Typography from '@mui/material/Typography'
import SelectAllIcon from '@mui/icons-material/SelectAll'
import UploadFileIcon from '@mui/icons-material/UploadFile'
import EditNoteIcon from '@mui/icons-material/EditNote'

import { listImages } from '../api/images'
import type { ImageListParams, ImageMetadata } from '../api/types'
import SearchBar from '../components/SearchBar'
import FilterPanel, {
  EMPTY_FILTERS,
  type FilterValues,
} from '../components/FilterPanel'
import ImageGrid from '../components/ImageGrid'
import ImageLightbox from '../components/ImageLightbox'
import EditMetadataDialog from '../components/EditMetadataDialog'
import BulkEditDialog from '../components/BulkEditDialog'
import ImportDialog from '../components/ImportDialog'
import ExportMenu from '../components/ExportMenu'
import { useAuth } from '../hooks/useAuth'

const PAGE_SIZE = 20

export default function GalleryPage() {
  const { user, logout } = useAuth()

  const [images, setImages] = useState<ImageMetadata[]>([])
  const [count, setCount] = useState(0)
  const [page, setPage] = useState(1)
  const [search, setSearch] = useState('')
  const [ordering, setOrdering] = useState('image_file_name')
  const [filters, setFilters] = useState<FilterValues>(EMPTY_FILTERS)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  // Selection state for bulk operations
  const [selected, setSelected] = useState<Set<string>>(new Set())
  const [selectMode, setSelectMode] = useState(false)

  // Dialog state
  const [previewIndex, setPreviewIndex] = useState(-1)
  const [editTarget, setEditTarget] = useState<string | null>(null)
  const [bulkOpen, setBulkOpen] = useState(false)
  const [importOpen, setImportOpen] = useState(false)

  const params: ImageListParams = useMemo(
    () => ({
      page,
      search: search || undefined,
      ordering: ordering || undefined,
      ...Object.fromEntries(
        Object.entries(filters).filter(([, v]) => v !== '')
      ),
    }),
    [page, search, ordering, filters]
  )

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await listImages(params)
      setImages(data.results)
      setCount(data.count)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to load images')
    } finally {
      setLoading(false)
    }
  }, [params])

  useEffect(() => {
    load()
  }, [load])

  // Reset to page 1 when search/filters change
  useEffect(() => {
    setPage(1)
  }, [search, filters, ordering])

  // Build filter dropdown options from the current result set.
  const filterOptions = useMemo(() => {
    const keys = Object.keys(EMPTY_FILTERS) as (keyof FilterValues)[]
    const opts = {} as Record<keyof FilterValues, string[]>
    for (const k of keys) {
      const vals = new Set<string>()
      for (const img of images) {
        const v = img[k]
        if (typeof v === 'string' && v.trim()) vals.add(v)
      }
      opts[k] = Array.from(vals).sort()
    }
    return opts
  }, [images])

  const handleSelect = (fileName: string, checked: boolean) => {
    setSelected((prev) => {
      const next = new Set(prev)
      if (checked) next.add(fileName)
      else next.delete(fileName)
      return next
    })
  }

  const selectAll = () =>
    setSelected(new Set(images.map((i) => i.image_file_name)))

  const clearSelection = () => {
    setSelected(new Set())
    setSelectMode(false)
  }

  const pageCount = Math.ceil(count / PAGE_SIZE)

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      <AppBar position="sticky">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            Image Gallery
          </Typography>
          {user ? (
            <>
              <Typography variant="body2" sx={{ mr: 2 }}>
                {user.username}
              </Typography>
              <Button color="inherit" onClick={logout}>
                Logout
              </Button>
            </>
          ) : (
            <Button color="inherit" href="/login">
              Login
            </Button>
          )}
        </Toolbar>
      </AppBar>

      <Container maxWidth="xl" sx={{ py: 3 }}>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mb: 3 }}>
          <SearchBar
            search={search}
            ordering={ordering}
            onSearchChange={setSearch}
            onOrderingChange={setOrdering}
          />
          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', alignItems: 'center' }}>
            <FilterPanel
              values={filters}
              options={filterOptions}
              onChange={setFilters}
            />
            <Box sx={{ flexGrow: 1 }} />
            <ExportMenu params={params} />
            {user && (
              <>
                <Button
                  size="small"
                  variant="outlined"
                  startIcon={<UploadFileIcon />}
                  onClick={() => setImportOpen(true)}
                >
                  Import
                </Button>
                <Button
                  size="small"
                  variant={selectMode ? 'contained' : 'outlined'}
                  startIcon={<SelectAllIcon />}
                  onClick={() => {
                    setSelectMode((v) => !v)
                    setSelected(new Set())
                  }}
                >
                  Select
                </Button>
              </>
            )}
            {selectMode && selected.size > 0 && (
              <>
                <Button size="small" onClick={selectAll}>
                  Select page ({images.length})
                </Button>
                <Button
                  size="small"
                  variant="contained"
                  color="secondary"
                  startIcon={<EditNoteIcon />}
                  onClick={() => setBulkOpen(true)}
                >
                  Bulk edit ({selected.size})
                </Button>
                <Button size="small" onClick={clearSelection}>
                  Clear
                </Button>
              </>
            )}
          </Box>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        )}

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
            <CircularProgress />
          </Box>
        ) : images.length === 0 ? (
          <Typography color="text.secondary" sx={{ py: 8, textAlign: 'center' }}>
            No images match your filters.
          </Typography>
        ) : (
          <>
            <ImageGrid
              images={images}
              selected={selected}
              selectable={selectMode}
              onSelect={handleSelect}
              onPreview={(img) =>
                setPreviewIndex(
                  images.findIndex(
                    (i) => i.image_file_name === img.image_file_name
                  )
                )
              }
              onEdit={(img) => setEditTarget(img.image_file_name)}
            />
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
              <Pagination
                count={pageCount}
                page={page}
                onChange={(_, p) => setPage(p)}
                color="primary"
              />
            </Box>
            <Typography
              variant="caption"
              color="text.secondary"
              sx={{ display: 'block', textAlign: 'center', mt: 1 }}
            >
              {count} images total
            </Typography>
          </>
        )}
      </Container>

      <ImageLightbox
        images={images}
        index={previewIndex}
        onClose={() => setPreviewIndex(-1)}
      />

      <EditMetadataDialog
        fileName={editTarget}
        open={editTarget !== null}
        onClose={(saved) => {
          setEditTarget(null)
          if (saved) load()
        }}
      />

      <BulkEditDialog
        fileNames={Array.from(selected)}
        open={bulkOpen}
        onClose={(updated) => {
          setBulkOpen(false)
          if (updated) {
            clearSelection()
            load()
          }
        }}
      />

      <ImportDialog
        open={importOpen}
        onClose={(imported) => {
          setImportOpen(false)
          if (imported) load()
        }}
      />
    </Box>
  )
}
