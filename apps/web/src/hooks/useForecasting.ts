import { useState, useEffect, useCallback } from 'react'
import { apiGet } from '../services/api'

export interface ForecastingItem {
  id: string
  name?: string
  status?: string
  [key: string]: unknown
}

export function useForecasting() {
  const [items, setItems] = useState<ForecastingItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: ForecastingItem[] }>(`/api/forecasting`)
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
