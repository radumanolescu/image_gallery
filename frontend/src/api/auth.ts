import { api, ensureCsrfCookie } from './client'
import type { User } from './types'

export async function login(username: string, password: string): Promise<User> {
  await ensureCsrfCookie()
  const { data } = await api.post<User>('/api/auth/login/', { username, password })
  return data
}

export async function logout(): Promise<void> {
  await ensureCsrfCookie()
  await api.post('/api/auth/logout/')
}

export async function getCurrentUser(): Promise<User | null> {
  try {
    const { data } = await api.get<User>('/api/auth/me/')
    return data
  } catch {
    return null
  }
}
