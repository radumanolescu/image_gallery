import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import FilterPanel, {
  EMPTY_FILTERS,
  type FilterValues,
} from './FilterPanel'

const OPTIONS: Record<keyof FilterValues, string[]> = {
  medium: ['oil', 'watercolor'],
  location: ['studio'],
  part_of_gallery: [],
  orientation: ['landscape', 'portrait'],
  substrate: ['canvas'],
  in_inventory: ['yes', 'no'],
  currently_shown: ['yes', 'no'],
}

function renderPanel(values: Partial<FilterValues> = {}) {
  const props = {
    values: { ...EMPTY_FILTERS, ...values },
    options: OPTIONS,
    onChange: vi.fn(),
  }
  render(<FilterPanel {...props} />)
  return props
}

describe('FilterPanel', () => {
  it('renders a collapsed Filters button by default', () => {
    renderPanel()
    expect(
      screen.getByRole('button', { name: 'Filters' })
    ).toBeInTheDocument()
    expect(screen.queryByLabelText('Medium')).not.toBeInTheDocument()
  })

  it('expands to reveal filter selects when clicked', async () => {
    renderPanel()
    await userEvent.click(screen.getByRole('button', { name: 'Filters' }))
    // One combobox per filter definition (7 fields)
    expect(screen.getAllByRole('combobox')).toHaveLength(7)
  })

  it('shows the count of active filters and a Clear all button', () => {
    renderPanel({ medium: 'oil', location: 'studio' })
    expect(
      screen.getByRole('button', { name: 'Filters (2)' })
    ).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Clear all' })
    ).toBeInTheDocument()
  })

  it('resets all filters when Clear all is clicked', async () => {
    const props = renderPanel({ medium: 'oil' })
    await userEvent.click(screen.getByRole('button', { name: 'Clear all' }))
    expect(props.onChange).toHaveBeenCalledWith(EMPTY_FILTERS)
  })

  it('calls onChange with the updated value when a filter is selected', async () => {
    const props = renderPanel()
    await userEvent.click(screen.getByRole('button', { name: 'Filters' }))
    // Comboboxes render in FILTER_DEFS order; the first is Medium
    await userEvent.click(screen.getAllByRole('combobox')[0])
    await userEvent.click(await screen.findByRole('option', { name: 'oil' }))
    expect(props.onChange).toHaveBeenCalledWith(
      expect.objectContaining({ medium: 'oil' })
    )
  })
})
