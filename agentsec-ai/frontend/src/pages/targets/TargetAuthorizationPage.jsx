import React, { useEffect, useState } from 'react'
import { CheckCircle2, Clipboard, ExternalLink, KeyRound, RefreshCw, ShieldCheck, Trash2 } from 'lucide-react'
import { api } from '../../api'

const INITIAL_FORM = {
  target: 'localhost:5174',
  method: 'http',
  reason: 'Development-local authorized target for testing the FOUND FIRST integration',
}

function normalizeTargetInput(value) {
  const trimmed = value.trim()
  try {
    const parsed = new URL(trimmed.includes('://') ? trimmed : `https://${trimmed}`)
    if (parsed.pathname !== '/' || parsed.search || parsed.hash) return trimmed
    return parsed.port ? `${parsed.hostname}:${parsed.port}` : parsed.hostname
  } catch {
    return trimmed
  }
}

function StatusPill({ verified }) {
  return <span className={`status status-${verified ? 'completed' : 'queued'}`}><i />{verified ? 'OWNERSHIP VERIFIED' : 'MANUALLY APPROVED'}</span>
}

export default function TargetAuthorizationPage() {
  const [form, setForm] = useState(INITIAL_FORM)
  const [challenge, setChallenge] = useState(null)
  const [ownershipVerified, setOwnershipVerified] = useState(false)
  const [targets, setTargets] = useState([])
  const [requests, setRequests] = useState([])
  const [loading, setLoading] = useState(false)
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')

  const loadTargets = async () => {
    try {
      setTargets(await api.targets())
      setRequests(await api.authorizationRequests())
      setError('')
    } catch (err) {
      setError(err.message)
    }
  }

  useEffect(() => { void loadTargets() }, [])

  const update = (key, value) => setForm(current => ({ ...current, [key]: value }))
  const createChallenge = async (event) => {
    event.preventDefault()
    setLoading(true); setError(''); setMessage('')
    try {
      const target = normalizeTargetInput(form.target)
      if (!target) throw new Error('Enter a domain or public IP address.')
      if (target !== form.target) setForm(current => ({ ...current, target }))
      const result = await api.createTargetVerification({ target, method: form.method })
      setChallenge(result)
      setOwnershipVerified(Boolean(result.auto_approved))
      setMessage(result.auto_approved
        ? 'Development-local target approved automatically.'
        : 'Challenge created. Complete the DNS or HTTPS step, then verify ownership.')
      if (result.auto_approved) await loadTargets()
    } catch (err) { setError(err.message) } finally { setLoading(false) }
  }
  const verify = async () => {
    setLoading(true); setError(''); setMessage('')
    try {
      const result = await api.verifyTarget({ target: normalizeTargetInput(form.target), method: form.method })
      if (!result.verified) throw new Error(result.detail || 'Ownership verification failed. Check the record and try again.')
      setOwnershipVerified(true)
      setMessage('Ownership verified. An administrator can now approve this target.')
      await loadTargets()
    } catch (err) { setError(err.message) } finally { setLoading(false) }
  }
  const submitRequest = async (event) => {
    event.preventDefault()
    setLoading(true); setError(''); setMessage('')
    try {
      await api.createAuthorizationRequest({
        target: normalizeTargetInput(form.target),
        reason: form.reason,
      })
      setMessage('Authorization request submitted for administrator review.')
      await loadTargets()
    } catch (err) { setError(err.message) } finally { setLoading(false) }
  }
  const revoke = async (target) => {
    setLoading(true); setError(''); setMessage('')
    try {
      await api.revokeTarget(target)
      setMessage(`${target} was revoked and can no longer be scanned.`)
      await loadTargets()
    } catch (err) { setError(err.message) } finally { setLoading(false) }
  }
  const copy = async () => {
    if (!challenge?.token) return
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(challenge.token)
      } else {
        const input = document.createElement('textarea')
        input.value = challenge.token
        input.setAttribute('readonly', '')
        input.style.position = 'fixed'
        input.style.opacity = '0'
        document.body.appendChild(input)
        input.select()
        document.execCommand('copy')
        input.remove()
      }
      setMessage('Verification token copied.')
    } catch {
      setError('The browser blocked clipboard access. Copy the token from the challenge text manually.')
    }
  }

  return <div className="page">
    <div className="page-toolbar">
      <div><span className="eyebrow red">SCOPE CONTROL</span><h2>TARGET AUTHORIZATION</h2><p className="muted">Verify ownership when possible, or submit a request for an explicit administrator decision.</p></div>
      <button className="btn outline" onClick={() => void loadTargets()} disabled={loading}><RefreshCw size={15} /> REFRESH</button>
    </div>
    {error && <p className="form-error">{error}</p>}
    {message && <p className="success-message"><CheckCircle2 size={15} />{message}</p>}
    <div className="operations-grid">
      <section className="panel">
        <div className="panel-heading"><div><span className="eyebrow">OPTIONAL VERIFICATION</span><h3>VERIFY OWNERSHIP</h3></div><ShieldCheck size={20} /></div>
        <form onSubmit={createChallenge}>
          <label className="authorization-field">TARGET DOMAIN OR PUBLIC IP<input value={form.target} onChange={event => update('target', event.target.value)} placeholder="owned-example.com" required /></label>
          <label className="authorization-field">VERIFICATION METHOD<select value={form.method} onChange={event => update('method', event.target.value)}><option value="dns_txt">DNS TXT RECORD</option><option value="http">HTTPS WELL-KNOWN FILE</option></select></label>
          <button className="btn primary" disabled={loading}><KeyRound size={15} /> CREATE CHALLENGE</button>
        </form>
        {challenge && <div className="rehearsal-card">
          <span className="eyebrow">PUBLISH THIS VALUE</span>
          <p className="mono">{challenge.instructions}</p>
          <div className="verification-token"><span>CURRENT TOKEN</span><code>{challenge.token}</code></div>
          <div className="button-row"><button type="button" className="btn outline" onClick={copy}><Clipboard size={15} /> COPY TOKEN</button><button type="button" className="btn primary" onClick={verify} disabled={loading}><ShieldCheck size={15} /> VERIFY NOW</button></div>
        </div>}
      </section>
      <section className="panel">
        <div className="panel-heading"><div><span className="eyebrow">MANUAL REVIEW</span><h3>REQUEST AUTHORIZATION</h3></div><span className="mono muted">ADMIN DECISION REQUIRED</span></div>
        <form onSubmit={submitRequest}>
          <label className="authorization-field">TARGET<input value={form.target} onChange={event => update('target', event.target.value)} placeholder="owned-example.com or https://github.com/owner/repo" required /></label>
          <label className="authorization-field">APPROVAL REASON<textarea value={form.reason} onChange={event => update('reason', event.target.value)} placeholder="Company-owned test environment" required rows="4" /></label>
          <p className="muted">Manual approval is recorded separately from ownership verification. Only an administrator may approve or reject this request.</p>
          <button className="btn primary" disabled={loading}><CheckCircle2 size={15} /> SUBMIT REQUEST</button>
        </form>
      </section>
    </div>
    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">REQUEST TRACKER</span><h3>AUTHORIZATION REQUESTS</h3></div><span className="mono muted">{requests.length} REQUESTS</span></div>
      {!requests.length && <p className="empty-state">No authorization requests have been submitted.</p>}
      {requests.map(request => <div className="task-row" key={request.id}><div><strong className="mono">{request.target}</strong><small>{request.reason}</small><small className="muted">REQUEST #{request.id} · {request.created_at || ''}</small></div><span className={`status status-${request.status === 'approved' ? 'completed' : request.status === 'rejected' ? 'failed' : 'queued'}`}><i />{request.status.toUpperCase()}</span></div>)}
    </section>
    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">ALLOWLIST</span><h3>APPROVED TARGETS</h3></div><span className="mono muted">{targets.length} TARGETS</span></div>
      {!targets.length && <p className="empty-state">No approved targets. Complete ownership verification and administrator approval above.</p>}
      {targets.map(target => <div className="task-row" key={target.id}><div><strong className="mono">{target.target}</strong><small className="muted">{target.reason}</small></div><div className="button-row"><StatusPill verified={target.ownership_verified} /><button className="icon-btn" title={`Revoke ${target.target}`} onClick={() => void revoke(target.target)} disabled={loading}><Trash2 size={16} /></button></div></div>)}
    </section>
    <p className="muted"><ExternalLink size={13} /> Only targets shown in this allowlist may be sent to the scan pipeline.</p>
  </div>
}
