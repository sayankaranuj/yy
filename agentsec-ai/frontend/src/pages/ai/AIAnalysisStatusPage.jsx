import React, { useEffect, useState } from 'react'
import { Activity, RefreshCw } from 'lucide-react'
import { api } from '../../api'

export default function AIAnalysisStatusPage() {
  const [status, setStatus] = useState(null)
  const [error, setError] = useState('')

  const load = async () => {
    try {
      setStatus(await api.aiStatus())
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  useEffect(() => { void load() }, [])

  return <div className="page">
    <div className="page-toolbar"><div><span className="eyebrow red">AI CONFIGURATION</span><h2>AI ANALYSIS</h2></div><button className="btn outline" onClick={() => void load()}><RefreshCw size={15} /> REFRESH</button></div>
    {error && <p className="form-error">{error}</p>}
    {status && <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">PROVIDER STATUS</span><h3>{status.available ? 'AVAILABLE' : 'NOT IMPLEMENTED'}</h3></div><Activity size={19} /></div>
      <p>{status.message}</p>
      <div className="database-status-grid">
        {status.providers.map(provider => <div key={provider.name}><span>{provider.name}</span><strong>{provider.configured ? 'API KEY CONFIGURED' : 'API KEY NOT CONFIGURED'}</strong></div>)}
      </div>
      <p className="muted">The current decision engine is rule-based. Adding an OpenAI or Anthropic key alone will not produce AI analysis until a provider integration is implemented.</p>
    </section>}
  </div>
}
