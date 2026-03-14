/**
 * Centralized API client for LedgerLive frontend.
 * Handles base URL, auth headers, and error handling.
 */

const BASE = typeof window !== 'undefined' ? '' : 'http://127.0.0.1:8090'

export async function apiClient<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const url = path.startsWith('http') ? path : `${BASE}${path}`
  const res = await fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })
  if (!res.ok) {
    const text = await res.text()
    throw new Error(`API ${res.status}: ${text || res.statusText}`)
  }
  return res.json() as Promise<T>
}

export const api = {
  get: <T>(path: string) => apiClient<T>(path, { method: 'GET' }),
  post: <T>(path: string, body?: unknown) =>
    apiClient<T>(path, { method: 'POST', body: body ? JSON.stringify(body) : undefined }),
  put: <T>(path: string, body?: unknown) =>
    apiClient<T>(path, { method: 'PUT', body: body ? JSON.stringify(body) : undefined }),
  delete: <T>(path: string) => apiClient<T>(path, { method: 'DELETE' }),
}
