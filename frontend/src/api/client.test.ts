import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'
import { afterAll, afterEach, beforeAll, describe, expect, it } from 'vitest'
import { api, imageUrl } from './client'

const server = setupServer()

beforeAll(() => server.listen({ onUnhandledRequest: 'error' }))
afterEach(() => {
  server.resetHandlers()
  // Clear cookies set during tests
  document.cookie.split(';').forEach((c) => {
    const name = c.split('=')[0].trim()
    document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/`
  })
})
afterAll(() => server.close())

describe('api client', () => {
  it('attaches the CSRF token header to mutating requests', async () => {
    document.cookie = 'csrftoken=test-token-123; path=/'
    let csrfHeader: string | null = null
    server.use(
      http.post('http://localhost:3000/api/test/', ({ request }) => {
        csrfHeader = request.headers.get('X-CSRFToken')
        return HttpResponse.json({ ok: true })
      })
    )
    await api.post('/api/test/', {})
    expect(csrfHeader).toBe('test-token-123')
  })

  it('does not attach a CSRF header to GET requests', async () => {
    document.cookie = 'csrftoken=test-token-123; path=/'
    let csrfHeader: string | null = 'unset'
    server.use(
      http.get('http://localhost:3000/api/test/', ({ request }) => {
        csrfHeader = request.headers.get('X-CSRFToken')
        return HttpResponse.json({ ok: true })
      })
    )
    await api.get('/api/test/')
    expect(csrfHeader).toBeNull()
  })
})

describe('imageUrl', () => {
  it('builds the media URL for a filename', () => {
    expect(imageUrl('IMG_0001.JPG')).toBe('/media/IMG_0001.JPG')
  })
})
