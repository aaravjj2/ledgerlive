import { useState, useEffect, useCallback } from 'react'
import { apiGet } from '../services/api'

export interface IntercompanyV2Item {
  id: string
  name?: string
  status?: string
  [key: string]: unknown
}

export function useIntercompanyV2() {
  const [items, setItems] = useState<IntercompanyV2Item[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: IntercompanyV2Item[] }>(`/api/intercompany-v2`)
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
