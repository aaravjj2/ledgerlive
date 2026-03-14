import { useState, useEffect, useCallback } from 'react'
import { apiGet } from '../services/api'

export interface AccrualsItem {
  id: string
  name?: string
  status?: string
  [key: string]: unknown
}

export function useAccruals() {
  const [items, setItems] = useState<AccrualsItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: AccrualsItem[] }>(`/api/accruals`)
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
