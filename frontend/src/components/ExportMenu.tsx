import { useState } from 'react'
import Button from '@mui/material/Button'
import Menu from '@mui/material/Menu'
import MenuItem from '@mui/material/MenuItem'
import ListItemIcon from '@mui/material/ListItemIcon'
import DownloadIcon from '@mui/icons-material/Download'
import { exportUrl } from '../api/images'
import type { ImageListParams } from '../api/types'

interface ExportMenuProps {
  params: ImageListParams
}

export default function ExportMenu({ params }: ExportMenuProps) {
  const [anchor, setAnchor] = useState<null | HTMLElement>(null)

  const openMenu = (e: React.MouseEvent<HTMLElement>) => setAnchor(e.currentTarget)
  const closeMenu = () => setAnchor(null)

  const go = (format: 'csv' | 'excel' | 'pdf') => {
    // Navigate to the export URL; the browser downloads the file.
    window.location.href = exportUrl(format, params)
    closeMenu()
  }

  return (
    <>
      <Button
        size="small"
        variant="outlined"
        startIcon={<DownloadIcon />}
        onClick={openMenu}
      >
        Export
      </Button>
      <Menu anchorEl={anchor} open={Boolean(anchor)} onClose={closeMenu}>
        <MenuItem onClick={() => go('csv')}>
          <ListItemIcon>
            <DownloadIcon fontSize="small" />
          </ListItemIcon>
          CSV
        </MenuItem>
        <MenuItem onClick={() => go('excel')}>
          <ListItemIcon>
            <DownloadIcon fontSize="small" />
          </ListItemIcon>
          Excel
        </MenuItem>
        <MenuItem onClick={() => go('pdf')}>
          <ListItemIcon>
            <DownloadIcon fontSize="small" />
          </ListItemIcon>
          PDF
        </MenuItem>
      </Menu>
    </>
  )
}
