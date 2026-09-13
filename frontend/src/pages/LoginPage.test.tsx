import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import { describe, expect, it, vi } from 'vitest'
import LoginPage from './LoginPage'
import { AuthProvider } from '../hooks/useAuth'
import * as authApi from '../api/auth'

vi.mock('../api/auth', () => ({
  login: vi.fn(),
  logout: vi.fn(),
  getCurrentUser: vi.fn().mockResolvedValue(null),
}))

function renderLogin() {
  return render(
    <MemoryRouter initialEntries={['/login']}>
      <AuthProvider>
        <LoginPage />
      </AuthProvider>
    </MemoryRouter>
  )
}

describe('LoginPage', () => {
  it('renders the login form', () => {
    renderLogin()
    expect(screen.getByLabelText(/^Username/)).toBeInTheDocument()
    expect(screen.getByLabelText(/^Password/)).toBeInTheDocument()
    expect(
      screen.getByRole('button', { name: 'Sign in' })
    ).toBeInTheDocument()
  })

  it('calls login with the entered credentials', async () => {
    vi.mocked(authApi.login).mockResolvedValue({
      username: 'admin',
      is_staff: true,
    })
    renderLogin()
    await userEvent.type(screen.getByLabelText(/^Username/), 'admin')
    await userEvent.type(screen.getByLabelText(/^Password/), 'secret')
    await userEvent.click(screen.getByRole('button', { name: 'Sign in' }))
    expect(authApi.login).toHaveBeenCalledWith('admin', 'secret')
  })

  it('shows an error message when login fails', async () => {
    vi.mocked(authApi.login).mockRejectedValue(new Error('401'))
    renderLogin()
    await userEvent.type(screen.getByLabelText(/^Username/), 'admin')
    await userEvent.type(screen.getByLabelText(/^Password/), 'wrong')
    await userEvent.click(screen.getByRole('button', { name: 'Sign in' }))
    expect(
      await screen.findByText('Invalid username or password')
    ).toBeInTheDocument()
  })
})
