export interface ImageMetadata {
  image_file_name: string
  invent_number: string | null
  invent_img: string | null
  high_res_image: string | null
  date: string | null
  id_title: string | null
  website_title: string | null
  part_of_gallery: string | null
  medium: string | null
  substrate: string | null
  dimensions_hxwxd: string | null
  orientation: string | null
  edition: string | null
  location: string | null
  in_inventory: string | null
  number_sold: number | null
  sale_price: string | null
  cost_of_goods: string | null
  current_inventory: number | null
  goods_sold: string | null
  currently_shown: string | null
  shown_in_past: string | null
  keywords: string | null
  created_at: string
  updated_at: string
}

export interface PaginatedResponse<T> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

export interface ImageListParams {
  page?: number
  search?: string
  ordering?: string
  medium?: string
  substrate?: string
  orientation?: string
  part_of_gallery?: string
  location?: string
  in_inventory?: string
  currently_shown?: string
}

export interface BulkUpdateRequest {
  image_file_names: string[]
  updates: Partial<ImageMetadata>
}

export interface BulkUpdateResponse {
  message: string
  updated_count: number
}

export interface BulkImportResponse {
  message: string
  imported_count: number
  errors: string[]
}

export interface User {
  username: string
  is_staff: boolean
}
