import { api, ensureCsrfCookie } from './client'
import type {
  BulkImportResponse,
  BulkUpdateRequest,
  BulkUpdateResponse,
  ImageListParams,
  ImageMetadata,
  PaginatedResponse,
} from './types'

export async function listImages(
  params: ImageListParams
): Promise<PaginatedResponse<ImageMetadata>> {
  const { data } = await api.get<PaginatedResponse<ImageMetadata>>(
    '/api/images/',
    { params }
  )
  return data
}

export async function getImage(fileName: string): Promise<ImageMetadata> {
  const { data } = await api.get<ImageMetadata>(
    `/api/images/${encodeURIComponent(fileName)}/`
  )
  return data
}

export async function updateImage(
  fileName: string,
  updates: Partial<ImageMetadata>
): Promise<ImageMetadata> {
  await ensureCsrfCookie()
  const { data } = await api.patch<ImageMetadata>(
    `/api/images/${encodeURIComponent(fileName)}/`,
    updates
  )
  return data
}

export async function bulkUpdate(
  request: BulkUpdateRequest
): Promise<BulkUpdateResponse> {
  await ensureCsrfCookie()
  const { data } = await api.post<BulkUpdateResponse>(
    '/api/images/bulk_update/',
    request
  )
  return data
}

export async function bulkImport(
  file: File,
  clearExisting = false
): Promise<BulkImportResponse> {
  await ensureCsrfCookie()
  const form = new FormData()
  form.append('file', file)
  form.append('clear_existing', String(clearExisting))
  const { data } = await api.post<BulkImportResponse>(
    '/api/images/bulk_import/',
    form,
    { headers: { 'Content-Type': 'multipart/form-data' } }
  )
  return data
}

// Export endpoints return file downloads. We navigate the browser to the
// URL so the download is handled natively (and current filters apply).
export function exportUrl(format: 'csv' | 'excel' | 'pdf', params?: ImageListParams): string {
  const path = `/api/images/export_${format === 'excel' ? 'excel' : format}/`
  const qs = new URLSearchParams()
  if (params) {
    for (const [k, v] of Object.entries(params)) {
      if (v !== undefined && v !== null && v !== '') qs.set(k, String(v))
    }
  }
  const s = qs.toString()
  return s ? `${path}?${s}` : path
}
