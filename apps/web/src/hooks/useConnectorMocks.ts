import { useState, useEffect, useCallback } from 'react'
import { apiGet } from '../services/api'

export interface ConnectorMocksItem {
  id: string
  name?: string
  status?: string
  [key: string]: unknown
}

export function useConnectorMocks() {
  const [items, setItems] = useState<ConnectorMocksItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: ConnectorMocksItem[] }>(`/api/connector-mocks`)
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
