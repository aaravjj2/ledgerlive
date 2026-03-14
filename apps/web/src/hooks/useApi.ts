/**
 * useApi — Generic API fetch hook with loading/error state.
 */
import { useState, useCallback } from 'react'

export function useApi<T>(url: string, options?: RequestInit) {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const fetchData = useCallback(async (overrideUrl?: string, overrideOpts?: RequestInit) => {
    setLoading(true)
    setError(null)
    try {
      const r = await fetch(overrideUrl ?? url, overrideOpts ?? options)
      const j = await r.json()
      setData(j)
      return j
    } catch (e) {
      const err = e instanceof Error ? e : new Error(String(e))
      setError(err)
      throw err
    } finally {
      setLoading(false)
    }
  }, [url, options])

  return { data, loading, error, fetchData }
}

export function useApiMutation<T, B = unknown>(url: string, method: string = 'POST') {
  const [data, setData] = useState<T | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<Error | null>(null)

  const mutate = useCallback(async (body?: B) => {
    setLoading(true)
    setError(null)
    setData(null)
    try {
      const r = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: body != null ? JSON.stringify(body) : undefined,
      })
      const j = await r.json()
      setData(j)
      return j
    } catch (e) {
      const err = e instanceof Error ? e : new Error(String(e))
      setError(err)
      throw err
    } finally {
      setLoading(false)
    }
  }, [url, method])

  return { data, loading, error, mutate }
}

export default useApi
