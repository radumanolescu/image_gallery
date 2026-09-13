import axios from 'axios'

// Reads the csrftoken cookie set by GET /api/auth/csrf/
function getCsrfToken(): string | null {
  const match = document.cookie.match(/(?:^|;\s*)csrftoken=([^;]+)/)
  return match ? decodeURIComponent(match[1]) : null
}

export const api = axios.create({
  baseURL: '/',
  withCredentials: true, // send session cookies
})

// Attach the CSRF token to every mutating request.
api.interceptors.request.use((config) => {
  const method = (config.method ?? 'get').toLowerCase()
  if (!['get', 'head', 'options', 'trace'].includes(method)) {
    const token = getCsrfToken()
    if (token) {
      config.headers['X-CSRFToken'] = token
    }
  }
  return config
})

// Prime the CSRF cookie before the first unsafe request.
export async function ensureCsrfCookie(): Promise<void> {
  if (!getCsrfToken()) {
    await api.get('/api/auth/csrf/')
  }
}

export function imageUrl(fileName: string): string {
  return `/media/${fileName}`
}
