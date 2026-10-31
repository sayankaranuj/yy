import React, { useState } from 'react'
import { ArrowRight, GitBranch, ShieldCheck } from 'lucide-react'
import { api } from '../../api'

export default function GitRepositoryPage({ scans, onScanCreated, onOpenScan }) {
  const [repository, setRepository] = useState('')
  const [name, setName] = useState('')
  const [branch, setBranch] = useState('')
  const [sinceCommit, setSinceCommit] = useState('')
  const [untilCommit, setUntilCommit] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')
  const gitScans = scans.filter(scan => scan.selected_attack_categories?.includes('secrets.git_scan'))

  const submit = async event => {
    event.preventDefault()
    setLoading(true)
    setError('')
    setMessage('')
    try {
      const scan = await api.createScan({
        name: name.trim() || `Git scan: ${repository.trim()}`,
        target: repository.trim(),
        selected_attack_categories: ['secrets.git_scan'],
        git_options: {
          ...(branch.trim() ? { branch: branch.trim() } : {}),
          ...(sinceCommit.trim() ? { since_commit: sinceCommit.trim() } : {}),
          ...(untilCommit.trim() ? { until_commit: untilCommit.trim() } : {}),
        },
      })
      setMessage(`Git scan #${scan.id} was queued. TruffleHog output will appear on its scan page.`)
      onScanCreated(scan)
      onOpenScan(scan)
      setRepository('')
      setName('')
      setBranch('')
      setSinceCommit('')
      setUntilCommit('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return <div className="page">
    <div className="page-toolbar">
      <div><span className="eyebrow red">SOURCE CODE SECURITY</span><h2>GIT REPOSITORY SCANNING</h2><p className="muted">Run TruffleHog against an explicitly approved public repository and inspect real findings.</p></div>
      <GitBranch size={20} />
    </div>
    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">SECRET DETECTION</span><h3>SCAN A PUBLIC REPOSITORY</h3></div><ShieldCheck size={19} /></div>
      <form onSubmit={submit}>
        <label className="authorization-field">HTTPS REPOSITORY URL<input type="url" value={repository} onChange={event => setRepository(event.target.value)} placeholder="https://github.com/owner/repository" required /></label>
        <label className="authorization-field">SCAN NAME<input value={name} onChange={event => setName(event.target.value)} placeholder="Optional descriptive name" /></label>
        <label className="authorization-field">BRANCH<input value={branch} onChange={event => setBranch(event.target.value)} placeholder="Optional branch (default repository HEAD)" /></label>
        <label className="authorization-field">SINCE COMMIT<input value={sinceCommit} onChange={event => setSinceCommit(event.target.value)} placeholder="Optional commit SHA" /></label>
        <label className="authorization-field">UNTIL COMMIT<input value={untilCommit} onChange={event => setUntilCommit(event.target.value)} placeholder="Optional commit SHA" /></label>
        <p className="muted">The exact repository URL must be approved in Authorization first. This flow supports public GitHub, GitLab, and Bitbucket repositories; private-repository credentials are not collected.</p>
        {error && <p className="form-error">{error}</p>}
        {message && <p className="success-message">{message}</p>}
        <button className="btn primary" disabled={loading}>{loading ? 'DISPATCHING...' : 'START GIT SCAN'} <ArrowRight size={15} /></button>
      </form>
    </section>
    <section className="panel">
      <div className="panel-heading"><div><span className="eyebrow">SCAN HISTORY</span><h3>REPOSITORY SCANS</h3></div><span className="mono muted">{gitScans.length} SCANS</span></div>
      {!gitScans.length && <p className="empty-state">No repository scans have been created.</p>}
      {gitScans.map(scan => <button type="button" className="task-row git-scan-row" key={scan.id} onClick={() => onOpenScan(scan)}>
        <span className={`status status-${scan.status}`}><i />{scan.status.toUpperCase()}</span>
        <span className="mono">{scan.target}</span>
        <small>SCAN #{scan.id}</small>
      </button>)}
    </section>
  </div>
}
