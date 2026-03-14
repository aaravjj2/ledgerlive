import { useState, useEffect, useCallback } from 'react'
import { apiGet } from '../services/api'

export interface JePostingItem {
  id: string
  name?: string
  status?: string
  [key: string]: unknown
}

export function useJePosting() {
  const [items, setItems] = useState<JePostingItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: JePostingItem[] }>(`/api/je-posting`)
      setItems(res?.items ?? [])
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed')
      setItems([])
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  return { items, loading, error, reload: load }
}
