import type { ImageMetadata } from '../api/types'

export function makeImage(
  overrides: Partial<ImageMetadata> = {}
): ImageMetadata {
  return {
    image_file_name: 'IMG_0001.JPG',
    invent_number: '12',
    invent_img: '1',
    high_res_image: null,
    date: '2020-01-15',
    id_title: 'Test Title',
    website_title: null,
    part_of_gallery: 'Landscapes',
    medium: 'oil',
    substrate: 'canvas',
    dimensions_hxwxd: '18x24',
    orientation: 'landscape',
    edition: null,
    location: 'studio',
    in_inventory: 'yes',
    number_sold: 0,
    sale_price: '250.00',
    cost_of_goods: '50.00',
    current_inventory: 1,
    goods_sold: null,
    currently_shown: 'no',
    shown_in_past: 'yes',
    keywords: 'test, sample',
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-02T00:00:00Z',
    ...overrides,
  }
}
