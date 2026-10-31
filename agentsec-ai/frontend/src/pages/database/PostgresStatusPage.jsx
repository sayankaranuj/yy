import React, { useCallback, useEffect, useState } from 'react'
import { Database, RefreshCw } from 'lucide-react'
import { api } from '../../api'

export default function PostgresStatusPage() {
  const [state, setState] = useState(null)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const load = useCallback(async () => {
    setLoading(true)
    try {
      setState(await api.databaseStatus())
      setError('')
    } catch (err) {
      setState(null)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { void load() }, [load])

  return <div className="page">
    <div className="page-toolbar">
      <div><span className="eyebrow">PERSISTENCE</span><h2>POSTGRESQL</h2><p className="muted">Read-only connection status for the database configured by the backend.</p></div>
      <button className="btn outline" onClick={() => void load()} disabled={loading}><RefreshCw size={15} /> REFRESH</button>
    </div>
    {error && <p className="form-error">{error}</p>}
    {state && <section className="panel database-status">
      <div className="panel-heading"><div><span className="eyebrow">DATABASE CONNECTION</span><h3>{state.status === 'connected' ? 'CONNECTED' : 'NOT CONNECTED'}</h3></div><Database size={20} /></div>
      <div className="database-status-grid">
        <div><span>STORAGE BACKEND</span><strong>{state.storage_backend}</strong></div>
        <div><span>DATABASE</span><strong>{state.database || 'Not configured'}</strong></div>
        <div><span>DATABASE USER</span><strong>{state.user || '—'}</strong></div>
        <div><span>SERVER</span><strong>{state.version || '—'}</strong></div>
      </div>
      <p className="muted">The page does not expose credentials or permit arbitrary SQL execution.</p>
    </section>}
  </div>
}
