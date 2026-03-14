import { useState, useEffect, useCallback } from 'react'
import { apiGet } from '../services/api'

export interface BankReconItem {
  id: string
  name?: string
  status?: string
  [key: string]: unknown
}

export function useBankRecon() {
  const [items, setItems] = useState<BankReconItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await apiGet<{ items?: BankReconItem[] }>(`/api/reconciliations`)
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
