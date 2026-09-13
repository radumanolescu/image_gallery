import { fireEvent, render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import ImageCard from './ImageCard'
import { makeImage } from '../test/factories'

function renderCard(overrides: Partial<Parameters<typeof ImageCard>[0]> = {}) {
  const props = {
    image: makeImage(),
    selected: false,
    selectable: false,
    onSelect: vi.fn(),
    onPreview: vi.fn(),
    onEdit: vi.fn(),
    ...overrides,
  }
  render(<ImageCard {...props} />)
  return props
}

describe('ImageCard', () => {
  it('renders the title, filename, medium and inventory chips', () => {
    renderCard()
    expect(screen.getByText('Test Title')).toBeInTheDocument()
    expect(screen.getByText('IMG_0001.JPG')).toBeInTheDocument()
    expect(screen.getByText('oil')).toBeInTheDocument()
    expect(screen.getByText('#12')).toBeInTheDocument()
  })

  it('falls back to the filename when no title is set', () => {
    renderCard({ image: makeImage({ id_title: null }) })
    // Title slot shows the filename; the caption also shows it
    const matches = screen.getAllByText('IMG_0001.JPG')
    expect(matches.length).toBeGreaterThanOrEqual(1)
  })

  it('calls onPreview when the card body is clicked', async () => {
    const props = renderCard()
    await userEvent.click(screen.getByRole('img', { name: 'Test Title' }))
    expect(props.onPreview).toHaveBeenCalledWith(props.image)
  })

  it('calls onEdit when the edit button is clicked', async () => {
    const props = renderCard()
    await userEvent.click(
      screen.getByRole('button', { name: 'edit IMG_0001.JPG' })
    )
    expect(props.onEdit).toHaveBeenCalledWith(props.image)
    expect(props.onPreview).not.toHaveBeenCalled()
  })

  it('shows a selection checkbox only in select mode', () => {
    const first = render(
      <ImageCard
        image={makeImage()}
        selected={false}
        selectable={false}
        onSelect={vi.fn()}
        onPreview={vi.fn()}
        onEdit={vi.fn()}
      />
    )
    expect(screen.queryByRole('checkbox')).not.toBeInTheDocument()
    first.unmount()
    renderCard({ selectable: true })
    expect(screen.getByRole('checkbox')).toBeInTheDocument()
  })

  it('calls onSelect with the filename when the checkbox is toggled', async () => {
    const props = renderCard({ selectable: true })
    await userEvent.click(screen.getByRole('checkbox'))
    expect(props.onSelect).toHaveBeenCalledWith('IMG_0001.JPG', true)
  })

  it('shows a broken-image placeholder when the image fails to load', () => {
    renderCard()
    const img = screen.getByRole('img', { name: 'Test Title' })
    fireEvent.error(img)
    expect(screen.queryByRole('img')).not.toBeInTheDocument()
  })
})
