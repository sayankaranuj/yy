import React, { useEffect, useState } from 'react'
import { CheckCircle2, RefreshCw, ShieldCheck, XCircle } from 'lucide-react'
import { api } from '../../api'

const statusText = value => String(value || '').replaceAll('_', ' ').toUpperCase()

export default function AdminAuthorizationPage() {
  const [requests, setRequests] = useState([])
  const [note, setNote] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  const load = async () => {
    setLoading(true)
    try {
      setRequests(await api.authorizationRequests())
      setError('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { void load() }, [])

  const review = async (requestId, decision) => {
    setLoading(true)
    setError('')
    setMessage('')
    try {
      await api.reviewAuthorizationRequest(requestId, { decision, note })
      setMessage(`Request #${requestId} ${decision === 'approve' ? 'approved' : 'rejected'}.`)
      await load()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const pending = requests.filter(request => request.status === 'pending')
  const reviewed = requests.filter(request => request.status !== 'pending')

  return <div className="page">
    <div className="page-toolbar">
      <div><span className="eyebrow red">ADMIN CONTROL</span><h2>AUTHORIZATION REQUESTS</h2><p className="muted">Approve only targets you are authorized to assess. Decisions are recorded with the admin account and timestamp.</p></div>
      <button className="btn outline" onClick={() => void load()} disabled={loading}><RefreshCw size={15} /> REFRESH</button>
    </div>
    <p className="muted">Access uses the configured ADMIN_USERNAME and ADMIN_PASSWORD from the backend .env file.</p>
    {error && <p className="form-error">{error}</p>}
    {message && <p className="success-message"><CheckCircle2 size={15} />{message}</p>}
    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">PENDING REVIEW</span><h3>{pending.length} REQUEST(S)</h3></div><ShieldCheck size={19} /></div>
      <label className="authorization-field">ADMIN REVIEW NOTE<input value={note} onChange={event => setNote(event.target.value)} placeholder="Optional decision context" /></label>
      {!pending.length && <p className="empty-state">No authorization requests are waiting for review.</p>}
      {pending.map(request => <article className="authorization-request" key={request.id}>
        <div className="authorization-request-main">
          <div className="panel-heading"><strong className="mono">{request.target}</strong><span className="status status-queued"><i />PENDING</span></div>
          <p>{request.reason}</p>
          <small className="muted">REQUEST #{request.id} · SUBMITTED BY {request.requested_by} · {request.created_at || 'TIME NOT RECORDED'}</small>
        </div>
        <div className="button-row">
          <button className="btn primary" onClick={() => void review(request.id, 'approve')} disabled={loading}><CheckCircle2 size={15} /> APPROVE</button>
          <button className="btn outline" onClick={() => void review(request.id, 'reject')} disabled={loading}><XCircle size={15} /> REJECT</button>
        </div>
      </article>)}
    </section>
    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">AUDIT HISTORY</span><h3>REVIEWED REQUESTS</h3></div><span className="mono muted">{reviewed.length} DECISIONS</span></div>
      {!reviewed.length && <p className="empty-state">No decisions have been recorded.</p>}
      {reviewed.map(request => <div className="task-row" key={request.id}>
        <div><strong className="mono">{request.target}</strong><small className="muted">{request.review_note || request.reason}</small><small className="muted">#{request.id} · {request.reviewed_by || 'unknown'} · {request.reviewed_at || 'time unavailable'}</small></div>
        <span className={`status status-${request.status === 'approved' ? 'completed' : 'failed'}`}><i />{statusText(request.status)}</span>
      </div>)}
    </section>
  </div>
}
