import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, expect, it, vi } from 'vitest'
import SearchBar from './SearchBar'

function renderSearchBar(overrides: Partial<Parameters<typeof SearchBar>[0]> = {}) {
  const props = {
    search: '',
    ordering: 'image_file_name',
    onSearchChange: vi.fn(),
    onOrderingChange: vi.fn(),
    ...overrides,
  }
  render(<SearchBar {...props} />)
  return props
}

describe('SearchBar', () => {
  it('debounces search input before calling onSearchChange', async () => {
    const props = renderSearchBar()
    fireEvent.change(screen.getByLabelText('Search'), {
      target: { value: 'watercolor' },
    })
    // Should not fire immediately
    expect(props.onSearchChange).not.toHaveBeenCalled()
    await waitFor(
      () => expect(props.onSearchChange).toHaveBeenCalledWith('watercolor'),
      { timeout: 1500 }
    )
  })

  it('clears the search via the clear button', async () => {
    const props = renderSearchBar({ search: 'existing' })
    const clearBtn = await screen.findByLabelText('clear search')
    await userEvent.click(clearBtn)
    expect(props.onSearchChange).toHaveBeenCalledWith('')
  })

  it('changes sort field via the Sort by select', async () => {
    const props = renderSearchBar()
    const selects = screen.getAllByRole('combobox')
    await userEvent.click(selects[0])
    await userEvent.click(await screen.findByRole('option', { name: 'Title' }))
    expect(props.onOrderingChange).toHaveBeenCalledWith('id_title')
  })

  it('toggles direction to descending and prefixes ordering with -', async () => {
    const props = renderSearchBar({ ordering: 'date' })
    const selects = screen.getAllByRole('combobox')
    await userEvent.click(selects[1])
    await userEvent.click(
      await screen.findByRole('option', { name: 'Descending' })
    )
    expect(props.onOrderingChange).toHaveBeenCalledWith('-date')
  })

  it('strips the - prefix when switching back to ascending', async () => {
    const props = renderSearchBar({ ordering: '-date' })
    const selects = screen.getAllByRole('combobox')
    await userEvent.click(selects[1])
    await userEvent.click(
      await screen.findByRole('option', { name: 'Ascending' })
    )
    expect(props.onOrderingChange).toHaveBeenCalledWith('date')
  })
})
