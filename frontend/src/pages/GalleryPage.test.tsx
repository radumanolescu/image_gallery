import { render, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it, vi, beforeEach } from 'vitest'
import GalleryPage from './GalleryPage'
import { AuthProvider } from '../hooks/useAuth'
import * as imagesApi from '../api/images'
import { makeImage } from '../test/factories'

vi.mock('../api/images', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../api/images')>()
  return { ...actual, listImages: vi.fn() }
})

vi.mock('../api/auth', () => ({
  login: vi.fn(),
  logout: vi.fn().mockResolvedValue(undefined),
  getCurrentUser: vi.fn().mockResolvedValue(null),
}))

function renderGallery() {
  return render(
    <MemoryRouter initialEntries={['/']}>
      <AuthProvider>
        <GalleryPage />
      </AuthProvider>
    </MemoryRouter>
  )
}

const PAGE = {
  count: 2,
  next: null,
  previous: null,
  results: [
    makeImage({ image_file_name: 'IMG_0001.JPG', id_title: 'First' }),
    makeImage({ image_file_name: 'IMG_0002.JPG', id_title: 'Second' }),
  ],
}

describe('GalleryPage', () => {
  beforeEach(() => {
    vi.mocked(imagesApi.listImages).mockResolvedValue(PAGE)
  })

  it('renders image cards from the API response', async () => {
    renderGallery()
    expect(await screen.findByText('First')).toBeInTheDocument()
    expect(screen.getByText('Second')).toBeInTheDocument()
    expect(screen.getByText('2 images total')).toBeInTheDocument()
  })

  it('requests page 1 with the default ordering', async () => {
    renderGallery()
    await screen.findByText('First')
    expect(imagesApi.listImages).toHaveBeenCalledWith(
      expect.objectContaining({ page: 1, ordering: 'image_file_name' })
    )
  })

  it('shows an error alert when loading fails', async () => {
    vi.mocked(imagesApi.listImages).mockRejectedValue(
      new Error('Network down')
    )
    renderGallery()
    expect(await screen.findByRole('alert')).toHaveTextContent('Network down')
  })

  it('shows an empty state when no images match', async () => {
    vi.mocked(imagesApi.listImages).mockResolvedValue({
      count: 0,
      next: null,
      previous: null,
      results: [],
    })
    renderGallery()
    expect(
      await screen.findByText('No images match your filters.')
    ).toBeInTheDocument()
  })

  it('shows a Login button for anonymous users', async () => {
    renderGallery()
    await screen.findByText('First')
    expect(screen.getByRole('link', { name: 'Login' })).toBeInTheDocument()
    // Edit controls are hidden from anonymous users
    expect(
      screen.queryByRole('button', { name: 'Import' })
    ).not.toBeInTheDocument()
  })
})
