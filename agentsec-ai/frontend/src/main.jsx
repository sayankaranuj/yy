import React, { useEffect, useMemo, useState } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes, useLocation, useNavigate } from 'react-router-dom'
import ForceGraph3D from 'react-force-graph-3d'
import { Activity, AlertTriangle, ArrowLeft, CheckCircle2, ChevronRight, ClipboardCheck, Database, FileText, GitBranch, LayoutDashboard, Menu, Plus, Radio, RefreshCw, ShieldAlert, ShieldCheck, X } from 'lucide-react'
import { api, downloadJson, downloadPdf, openEventStream } from './api'
import ScanResultsPanel from './components/scans/ScanResultsPanel'
import TargetAuthorizationPage from './pages/targets/TargetAuthorizationPage'
import AdminAuthorizationPage from './pages/admin/AdminAuthorizationPage'
import PostgresStatusPage from './pages/database/PostgresStatusPage'
import GitRepositoryPage from './pages/git/GitRepositoryPage'
import AIAnalysisStatusPage from './pages/ai/AIAnalysisStatusPage'
import './index.css'

const EMPTY = { scans: [], findings: [], reports: [], dashboard: { scan_count: 0, finding_count: 0, high_severity_findings: 0, recent_scans: [] } }
const severityValues = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']

function SeverityBadge({ value = 'INFO' }) { return <span className={`severity severity-${value.toLowerCase()}`}><i />{value}</span> }
function ProgressBar({ value = 0 }) { return <div className="progress"><span style={{ width: `${Math.max(0, Math.min(100, value))}%` }} /></div> }
function ScanModeBadge({ mode = 'CLASSIC' }) { return <span className={`mode mode-${mode.toLowerCase()}`}>{mode}</span> }
function formatStatus(value = '') { return value.replaceAll('_', ' ').toUpperCase() }
function eventKey(event) {
  return event.event_id || `${event.event || ''}|${event.scan_id || ''}|${event.task_id || ''}|${event.tool_name || ''}|${event.line || ''}|${event.exit_code ?? ''}|${event.status || ''}|${event.records ?? ''}`
}
function Login({ onLogin }) {
  const [username, setUsername] = useState('admin')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const submit = async (event) => {
    event.preventDefault()
    try {
      const result = await api.login({ username, password })
      window.localStorage.setItem('agentsec_token', result.token)
      if (result.refresh_token) window.localStorage.setItem('agentsec_refresh_token', result.refresh_token)
      onLogin()
    } catch (err) { setError(err.message) }
  }
  return <div className="modal-backdrop"><form className="modal" onSubmit={submit}><span className="eyebrow red">SECURE ACCESS</span><h2>OPERATOR LOGIN</h2><label>USERNAME<input value={username} onChange={e => setUsername(e.target.value)} required /></label><label>PASSWORD<input type="password" value={password} onChange={e => setPassword(e.target.value)} required /></label>{error && <p className="form-error">{error}</p>}<button className="btn primary">SIGN IN <ChevronRight size={15} /></button></form></div>
}

function Sidebar({ page, setPage, compact, setCompact, onLogout }) {
  const items = [['overview', LayoutDashboard, 'OVERVIEW'], ['scans', Radio, 'SCANS'], ['git', GitBranch, 'GIT REPOSITORIES'], ['findings', ShieldAlert, 'FINDINGS'], ['ai', Activity, 'AI ANALYSIS'], ['reports', FileText, 'REPORTS'], ['targets', ShieldCheck, 'AUTHORIZATION'], ['admin', ClipboardCheck, 'ADMIN REVIEW'], ['postgres', Database, 'POSTGRESQL']]
  return <aside className={`sidebar ${compact ? 'compact' : ''}`}><button className="brand" onClick={() => setCompact(!compact)} aria-label="Toggle navigation"><span className="brand-mark">F</span>{!compact && <span>FOUND <span>FIRST</span></span>}<Menu size={16} /></button><nav>{items.map(([id, Icon, label]) => <button key={id} className={page === id ? 'nav-active' : ''} onClick={() => setPage(id)} title={label}><Icon size={18} /><span>{label}</span></button>)}</nav><div className="sidebar-bottom"><span className="operator"><b>OP</b>{!compact && <span>OPERATOR<br /><small>ONLINE</small></span>}</span><button className="text-action logout-action" onClick={onLogout} title="Log out"><span>LOG OUT</span></button></div></aside>
}
function Topbar({ title, onRefresh, loading }) { return <header className="topbar"><div><span className="eyebrow">SECURITY OPERATIONS / LIVE</span><h1>{title}</h1></div><div className="top-actions"><button className="icon-btn" title="Refresh data" onClick={onRefresh} disabled={loading}><RefreshCw size={17} /></button><div className="system-status"><i />{loading ? 'SYNCING DATA' : 'API CONNECTED'}</div></div></header> }
function StatCard({ label, value, detail, tone = '' }) { return <article className={`stat-card ${tone}`}><span className="stat-label"><i />{label}</span><strong>{value}</strong><small>{detail}</small></article> }
function ScanTable({ scans, onSelect }) { return <div className="table-wrap"><table><thead><tr><th>TARGET</th><th>STATUS</th><th>MODE</th><th>PROGRESS</th><th>LAST EVENT</th></tr></thead><tbody>{scans.map(scan => <tr key={scan.id} onClick={() => onSelect?.(scan)} className={scan.status === 'running' ? 'row-live' : ''}><td className="mono">{scan.target}</td><td><span className={`status status-${scan.status}`}><i />{formatStatus(scan.status)}</span></td><td><ScanModeBadge mode={scan.mode || 'CLASSIC'} /></td><td><ProgressBar value={scan.progress ?? (scan.status === 'completed' ? 100 : 0)} /></td><td className="muted">{scan.updated_at || scan.time || 'LIVE'}</td></tr>)}</tbody></table>{!scans.length && <p className="empty-state">No scans recorded yet.</p>}</div> }
function AttackSelector({ catalog, catalogError, onRetry, selected, onToggle }) {
  if (!catalog) return <section className="scan-selector-panel"><div className="panel-heading"><div><span className="eyebrow">ATTACK PLAN</span><h3>ATTACK CATEGORIES</h3></div>{catalogError ? <button className="text-action" onClick={onRetry}>RETRY CATALOG</button> : <span className="mono muted">LOADING CATALOG...</span>}</div>{catalogError && <p className="selector-description form-error">{catalogError}</p>}</section>
  return <section className="scan-selector-panel"><div className="panel-heading"><div><span className="eyebrow">ATTACK PLAN / OPTIONAL</span><h3>ATTACK CATEGORIES</h3></div><span className="selector-count">{selected.length} SELECTED</span></div><p className="selector-description">Choose specific checks for the next operation. Leave empty to use the normal decision engine.</p><div className="page-attack-grid">{Object.entries(catalog).map(([group, data]) => <div className="page-attack-group" key={group}><strong>{data.label}</strong><div className="page-attack-options">{Object.entries(data.items).map(([key, label]) => <label className="page-checkbox" key={key}><input type="checkbox" checked={selected.includes(key)} onChange={() => onToggle(key)} /><span>{label}</span></label>)}</div></div>)}</div></section>
}
function CreateScan({ onClose, onCreated, selectedAttackCategories }) {
  const [name, setName] = useState('')
  const [target, setTarget] = useState('')
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)
  useEffect(() => {
    const previousOverflow = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    document.documentElement.style.overflow = 'hidden'
    return () => {
      document.body.style.overflow = previousOverflow
      document.documentElement.style.overflow = ''
    }
  }, [])
  const submit = async (event) => {
    event.preventDefault(); setSaving(true); setError('')
    try {
      const payload = { name, target }
      if (selectedAttackCategories.length) payload.selected_attack_categories = selectedAttackCategories
      const scan = await api.createScan(payload); onCreated(scan); onClose()
    } catch (err) { setError(err.message) } finally { setSaving(false) }
  }
  return <div className="modal-backdrop" role="dialog"><form className="modal" onSubmit={submit}>
    <button type="button" className="icon-btn modal-close" onClick={onClose} aria-label="Close"><X size={18} /></button>
    <div className="modal-heading"><div><span className="eyebrow red">NEW OPERATION</span><h2>START SCAN</h2><p>Configure a scoped security operation.</p></div><span className="modal-index">01 / 03</span></div>
    <div className="modal-body">
    <label>NAME<input value={name} onChange={e => setName(e.target.value)} required placeholder="Production perimeter" /></label>
    <label>TARGET<input value={target} onChange={e => setTarget(e.target.value)} required placeholder="example.com" /></label>
    {error && <p className="form-error">{error}</p>}
    </div><div className="modal-footer"><span className="modal-safe"><i /> AUTHORIZED SCOPE REQUIRED</span><button className="btn primary" disabled={saving}>{saving ? 'DISPATCHING...' : 'DISPATCH SCAN'} <ChevronRight size={15} /></button></div>
  </form></div>
}
function Overview({ data, setPage }) { const d = data.dashboard; return <div className="page"><section className="hero siege-surface"><div><span className="eyebrow red">LIVE SECURITY POSTURE</span><h2>THE NETWORK<br /><em>IS WATCHING.</em></h2><p>Attack surface intelligence, without the noise.</p></div><div className="hero-readout"><span>OPEN FINDINGS</span><strong>{String(d.finding_count).padStart(2, '0')}</strong><small>{d.high_severity_findings} high severity</small></div></section><div className="stats-grid"><StatCard label="TOTAL SCANS" value={String(d.scan_count).padStart(2, '0')} detail="Persisted operations" /><StatCard label="OPEN FINDINGS" value={String(d.finding_count).padStart(2, '0')} detail="Current inventory" /><StatCard label="HIGH SEVERITY" value={String(d.high_severity_findings).padStart(2, '0')} detail="Needs attention" tone="critical" /><StatCard label="API STATE" value="LIVE" detail="Backend connected" tone="active" /></div><section className="section-block"><div className="section-heading"><div><span className="eyebrow">OPERATIONS FEED</span><h3>RECENT SCANS</h3></div><button className="text-action" onClick={() => setPage('scans')}>VIEW ALL <ChevronRight size={15} /></button></div><ScanTable scans={d.recent_scans} onSelect={() => setPage('scans')} /></section></div> }
function ListControls({ search, setSearch, status, setStatus, statuses = [] }) {
  return <div className="list-controls" role="search">
    <input aria-label="Search records" placeholder="Search..." value={search} onChange={event => setSearch(event.target.value)} />
    <select aria-label="Filter by status" value={status} onChange={event => setStatus(event.target.value)}>
      <option value="ALL">All statuses</option>{statuses.map(value => <option key={value} value={value}>{formatStatus(value)}</option>)}
    </select>
  </div>
}
function Pager({ page, setPage, total, pageSize = 10 }) {
  const pages = Math.max(1, Math.ceil(total / pageSize))
  return <div className="pager"><button className="text-action" disabled={page <= 1} onClick={() => setPage(page - 1)}>PREVIOUS</button><span className="mono muted">PAGE {page} / {pages}</span><button className="text-action" disabled={page >= pages} onClick={() => setPage(page + 1)}>NEXT</button></div>
}
function Scans({ scans, setShowCreate, catalog, catalogError, onRetry, selected, setSelected, onSelect }) {
  const [search, setSearch] = useState('')
  const [status, setStatus] = useState('ALL')
  const [page, setPage] = useState(1)
  const filtered = scans.filter(scan => (!search || `${scan.target} ${scan.name || ''}`.toLowerCase().includes(search.toLowerCase())) && (status === 'ALL' || scan.status === status))
  const visible = filtered.slice((page - 1) * 10, page * 10)
  const toggle = (key) => setSelected(current => current.includes(key) ? current.filter(item => item !== key) : [...current, key])
  return <div className="page"><div className="page-toolbar"><div><span className="eyebrow">PIPELINE CONTROL</span><h2>SCANS</h2></div><button className="btn primary" onClick={() => setShowCreate(true)}><Plus size={15} /> NEW SCAN</button></div><AttackSelector catalog={catalog} catalogError={catalogError} onRetry={onRetry} selected={selected} onToggle={toggle} /><ListControls search={search} setSearch={value => { setSearch(value); setPage(1) }} status={status} setStatus={value => { setStatus(value); setPage(1) }} statuses={[...new Set(scans.map(scan => scan.status))]} /><ScanTable scans={visible} onSelect={onSelect} /><Pager page={page} setPage={setPage} total={filtered.length} /><section className="active-banner"><Radio size={20} /><div><span className="eyebrow red">LIVE OPERATIONS</span><strong>{scans.filter(s => s.status === 'running' || s.status === 'queued').length} scan(s) in progress</strong></div></section></div>
}
function Findings({ findings }) { const [filter, setFilter] = useState('ALL'); const [search, setSearch] = useState(''); const [status, setStatus] = useState('ALL'); const [page, setPage] = useState(1); const filtered = findings.filter(f => (!search || `${f.title} ${f.description || ''} ${f.affected_url || ''}`.toLowerCase().includes(search.toLowerCase())) && (filter === 'ALL' || formatStatus(f.severity) === filter) && (status === 'ALL' || f.status === status)); const visible = filtered.slice((page - 1) * 10, page * 10); return <div className="page"><div className="page-toolbar"><div><span className="eyebrow">THREAT INVENTORY</span><h2>FINDINGS</h2><p className="muted">Records persisted from real scanner outputs; no sample findings are generated.</p></div><button className="btn outline" onClick={() => downloadJson('found-first-findings.json', findings)}><FileText size={15} /> EXPORT</button></div><div className="severity-row">{severityValues.map(value => <button key={value} className={`severity-filter ${filter === value ? 'selected' : ''}`} onClick={() => { setFilter(filter === value ? 'ALL' : value); setPage(1) }}><SeverityBadge value={value} /><strong>{findings.filter(f => formatStatus(f.severity) === value).length}</strong></button>)}</div><ListControls search={search} setSearch={value => { setSearch(value); setPage(1) }} status={status} setStatus={value => { setStatus(value); setPage(1) }} statuses={[...new Set(findings.map(f => f.status))]} /><div className="table-wrap findings-table"><table><caption className="sr-only">Persisted security findings</caption><thead><tr><th>ID</th><th>FINDING</th><th>SCAN</th><th>SEVERITY</th><th>STATE</th></tr></thead><tbody>{visible.map(f => <tr key={f.id}><td className="mono muted">{f.id}</td><td><strong>{f.title}</strong>{f.description && <small className="finding-description">{f.description}</small>}{f.affected_url && <small className="mono muted">{f.affected_url}</small>}</td><td className="mono">{f.scan_id ? `#${f.scan_id}` : '—'}</td><td><SeverityBadge value={f.severity} /></td><td><span className={`status status-${f.status}`}><i />{formatStatus(f.status)}</span></td></tr>)}</tbody></table>{!filtered.length && <p className="empty-state">No real findings have been recorded for this filter.</p>}</div><Pager page={page} setPage={setPage} total={filtered.length} /></div> }
function ReportDetails({ scanId, onBack }) {
  const [report, setReport] = useState(null)
  const [error, setError] = useState('')
  useEffect(() => {
    let alive = true
    api.report(scanId).then(value => { if (alive) setReport(value) }).catch(err => { if (alive) setError(err.message) })
    return () => { alive = false }
  }, [scanId])
  if (error) return <div className="page"><button className="text-action" onClick={onBack}><ArrowLeft size={15} /> REPORTS</button><p className="form-error">{error}</p></div>
  if (!report) return <div className="page"><p className="empty-state">Loading persisted report for scan #{scanId}…</p></div>
  return <div className="page">
    <div className="page-toolbar"><div><button className="text-action" onClick={onBack}><ArrowLeft size={15} /> ALL REPORTS</button><span className="eyebrow red">SCAN #{report.scan_id}</span><h2>{report.target}</h2><p className="muted">{formatStatus(report.status)} · {report.summary.step_count} tasks · {report.summary.finding_count} findings</p></div><div className="top-actions"><button className="btn outline" onClick={() => downloadJson(`scan-${report.scan_id}-report.json`, report)}><FileText size={15} /> EXPORT JSON</button><button className="btn outline" onClick={() => downloadPdf(`scan-${report.scan_id}-report.pdf`, `/reports/${report.scan_id}/pdf`)}>PDF</button></div></div>
    <section className="panel report-summary-panel"><div className="panel-heading"><h3>EXECUTIVE SUMMARY</h3><span className={`status status-${report.status}`}><i />{formatStatus(report.status)}</span></div><p>{report.executive_summary?.headline || report.summary.message}</p><div className="report-metadata"><div><small>Scope</small><strong>{report.scope?.target || report.target}</strong></div><div><small>Coverage</small><strong>{report.executive_summary?.coverage || 'Not available'}</strong></div><div><small>Started</small><strong>{report.timeline?.started_at || 'Not recorded'}</strong></div><div><small>Ended</small><strong>{report.timeline?.ended_at || 'Not recorded'}</strong></div></div><details><summary>Scan configuration and authorization</summary><pre className="report-json">{JSON.stringify({ authorization: report.scope?.authorization_record, configuration: report.scan_configuration }, null, 2)}</pre></details></section>
    <section className="panel"><div className="panel-heading"><h3>EXECUTION STEPS</h3><span className="mono muted">{report.steps.length} RECORDED</span></div>
      {!report.steps.length && <p className="empty-state">This scan has no persisted worker tasks yet.</p>}
      {report.steps.map(step => <article className="report-step" key={`${step.task_id}:${step.task_name}`}>
        <div className="report-step-heading"><span className={`status status-${step.status}`}><i />{formatStatus(step.status)}</span><strong>{step.task_name}</strong><small className="mono muted">{step.task_id || 'Task ID pending'}</small></div>
        {step.commands.map(command => <div className="report-command" key={command}><span>COMMAND</span><code>{command}</code></div>)}
        <small className="muted">Duration: {step.duration_ms ?? 'not recorded'} ms · Retries: {step.retries || 0} · Worker: {step.worker_hostname || 'not recorded'}</small>
        {step.error && <p className="form-error">{step.error}</p>}
        {step.result !== null && step.result !== undefined && <details><summary>Actual worker result · {step.result_status || 'stored'}</summary><pre className="report-json">{JSON.stringify(step.result, null, 2)}</pre></details>}
        {!step.result && !step.error && <p className="muted">No worker result has been persisted for this stage yet.</p>}
      </article>)}
    </section>
    <section className="panel"><div className="panel-heading"><h3>FAILED / SKIPPED CHECKS</h3></div>{[...(report.failed_checks || []), ...(report.skipped_checks || [])].map(step => <p className="task-row" key={`${step.task_id}-${step.task_name}`}><strong>{step.task_name}</strong><span className={`status status-${step.status}`}><i />{formatStatus(step.status)}</span></p>)}{!(report.failed_checks?.length || report.skipped_checks?.length) && <p className="empty-state">No failed or skipped checks were recorded.</p>}<p className="muted">{(report.coverage_limitations || []).join(' ')}</p></section>
    <section className="panel"><div className="panel-heading"><h3>FINDINGS FROM THIS SCAN</h3><span className="mono muted">{report.findings.length}</span></div>
      {report.findings.map(finding => <div className="task-row" key={finding.id}><div><strong>{finding.title}</strong><small>{finding.description || 'No additional description was returned by the scanner.'}</small><small>Confidence: {finding.confidence || 'Not provided'} · CWE: {finding.cwe || 'Not mapped'} · OWASP: {finding.owasp_category || 'Not mapped'}</small>{finding.affected_url && <small className="mono">{finding.affected_url}</small>}{finding.evidence && <details><summary>Raw evidence and reproduction</summary><pre className="report-json">{JSON.stringify(finding.evidence, null, 2)}</pre></details>}<small>Remediation: {finding.remediation || 'Review the affected component and retest.'}</small></div><SeverityBadge value={finding.severity} /></div>)}
      {!report.findings.length && <p className="empty-state">{report.summary.message}</p>}
    </section>
  </div>
}
function Reports({ reports }) {
  const [selectedScanId, setSelectedScanId] = useState(null)
  const [search, setSearch] = useState('')
  const [status, setStatus] = useState('ALL')
  const [page, setPage] = useState(1)
  if (selectedScanId !== null) return <ReportDetails scanId={selectedScanId} onBack={() => setSelectedScanId(null)} />
  const filtered = reports.filter(report => (!search || report.target.toLowerCase().includes(search.toLowerCase())) && (status === 'ALL' || report.summary.status === status))
  const visible = filtered.slice((page - 1) * 10, page * 10)
  return <div className="page"><div className="page-toolbar"><div><span className="eyebrow">GENERATED INTELLIGENCE</span><h2>REPORTS</h2></div><button className="btn outline" onClick={() => downloadJson('found-first-reports.json', reports)}><FileText size={15} /> DOWNLOAD INDEX</button></div><ListControls search={search} setSearch={value => { setSearch(value); setPage(1) }} status={status} setStatus={value => { setStatus(value); setPage(1) }} statuses={[...new Set(reports.map(report => report.summary.status))]} /><div className="report-grid">{visible.map(report => <button type="button" className="report-card report-card-button" key={report.scan_id} onClick={() => setSelectedScanId(report.scan_id)}><div className="report-top"><FileText size={20} /><ScanModeBadge mode="CLASSIC" /></div><span className="eyebrow">SECURITY ASSESSMENT · SCAN #{report.scan_id}</span><h3>{report.target}</h3><p>{report.summary.findings_count} findings · {report.summary.steps} workflow steps</p><div className="report-meta"><span>{formatStatus(report.summary.status)}</span><span className="text-action">VIEW DETAILS <ChevronRight size={14} /></span></div></button>)}</div>{!filtered.length && <p className="empty-state">No reports match the selected filters.</p>}<Pager page={page} setPage={setPage} total={filtered.length} /></div>
}
function AgentStatus({ name, status, tasks = [] }) { const done = tasks.filter(task => task.status === 'completed').length; return <div className="agent-status"><i className={`status-dot status-${status}`} /><span>{name}</span><small>{tasks.length ? `${done}/${tasks.length} TASKS · ${formatStatus(status)}` : formatStatus(status)}</small></div> }
function stageStatus(tasks, stage) {
  const statuses = tasks.filter(task => task.task_name.includes(stage)).map(task => task.status)
  if (!statuses.length) return 'skipped'
  if (statuses.includes('running')) return 'running'
  if (statuses.includes('retrying')) return 'retrying'
  if (statuses.includes('queued')) return 'queued'
  if (statuses.includes('failed')) return 'failed'
  return statuses.every(status => status === 'completed') ? 'completed' : 'unknown'
}
function AttackGraph({ workflow }) {
  const nodes = (workflow?.tasks || []).map((task, index) => ({ id: task.task_id, name: task.task_name, status: task.status, group: index }))
  const links = nodes.slice(1).map((node, index) => ({ source: nodes[index].id, target: node.id }))
  return <div className="graph-panel graph-3d"><ForceGraph3D width={720} height={300} graphData={{ nodes, links }} backgroundColor="rgba(0,0,0,0)" nodeLabel={node => `${node.name}: ${node.status}`} nodeColor={node => node.status === 'completed' ? '#54d18a' : node.status === 'running' ? '#f1c75b' : '#7b8794'} linkColor={() => '#46505c'} linkDirectionalParticles={2} linkDirectionalParticleSpeed={0.004} nodeResolution={12} /></div>
}
function TerminalEvent({ event }) {
  if (event.event === 'tool.command_started') {
    return <div className="terminal-command"><span className="terminal-prompt">$</span><code>{event.command}</code><b>RUNNING</b></div>
  }
  if (event.event === 'tool.command_finished') {
    return <div className={`terminal-exit ${event.status === 'failed' ? 'failed' : ''}`}><span>{event.tool_name}</span><span>{event.status === 'failed' ? `FAILED${event.exit_code !== undefined ? ` · EXIT ${event.exit_code}` : ''}` : `EXIT ${event.exit_code}`}</span>{event.error && <code>{event.error}</code>}</div>
  }
  if (event.event === 'tool.terminal_line') {
    return <div className={`terminal-output terminal-${event.stream || 'stdout'}`}><span>{event.stream === 'stderr' ? 'ERR' : 'OUT'}</span><code>{event.line}</code></div>
  }
  return <div className="terminal-event"><span>{event.event || 'EVENT'}</span><code>{JSON.stringify(event)}</code></div>
}
function ScanDetail({ scan, onBack, navigate }) {
  const [workflow, setWorkflow] = useState({ tasks: [], results: [], status: scan.status })
  const [results, setResults] = useState([])
  const [workflowError, setWorkflowError] = useState('')
  const [resultsError, setResultsError] = useState('')
  const [events, setEvents] = useState([])
  const [actionError, setActionError] = useState('')
  const [agent, setAgent] = useState('overview')
  const location = useLocation()
  useEffect(() => {
    let alive = true
    const load = async () => {
      const [workflowResponse, resultsResponse] = await Promise.allSettled([
        api.workflow(scan.id),
        api.scanResults(scan.id),
      ])
      if (!alive) return
      if (workflowResponse.status === 'fulfilled') {
        setWorkflow(workflowResponse.value)
        setWorkflowError('')
      } else {
        setWorkflowError(workflowResponse.reason.message)
      }
      if (resultsResponse.status === 'fulfilled') {
        setResults(resultsResponse.value)
        setResultsError('')
      } else {
        setResultsError(resultsResponse.reason.message)
      }
    }
    void load()
    const timer = window.setInterval(load, 2000)
    const stop = openEventStream((event) => setEvents(current => {
      const key = eventKey(event)
      if (current.some(item => eventKey(item) === key)) return current
      return [...current.slice(-199), event]
    }), undefined, scan.id)
    return () => { alive = false; window.clearInterval(timer); stop() }
  }, [scan.id])
  useEffect(() => { setAgent(location.pathname.split('/')[3] || 'overview') }, [location.pathname])
  const activeTasks = workflow.tasks.filter(task => agent === 'overview' || task.task_name.includes(agent))
  const taskStatuses = workflow.tasks.map(task => task.status)
  const resultByTask = new Map(results.map(result => [result.tool_name, result]))
  const selectAgent = (item) => {
    setAgent(item)
    navigate(item === 'overview' ? `/scans/${scan.id}` : `/scans/${scan.id}/${item}`)
  }
  const changeScanState = async (action) => {
    setActionError('')
    try {
      const updated = await action(scan.id)
      setWorkflow(current => ({ ...current, status: updated.status }))
    } catch (error) {
      setActionError(error.message)
    }
  }
  return <div className="page scan-detail">
    <div className="page-toolbar"><div><button className="text-action" onClick={onBack}>← ALL SCANS</button><span className="eyebrow red">LIVE OPERATION</span><h2>{scan.target}</h2><p className="muted mono">SCAN #{scan.id} · {formatStatus(workflow.status)}</p></div><div className="top-actions">{['queued', 'running', 'cancel_requested'].includes(workflow.status) && <button className="btn outline" onClick={() => changeScanState(api.cancelScan)}>CANCEL</button>}{['failed', 'partial', 'cancelled'].includes(workflow.status) && <button className="btn outline" onClick={() => changeScanState(api.resumeScan)}>RESUME</button>}<ScanModeBadge mode={scan.mode || 'CLASSIC'} /></div></div>
    {actionError && <p className="form-error">{actionError}</p>}
    <div className="agent-tabs">{['overview', 'recon', 'enum', 'vuln', 'secrets', 'report'].map(item => <button key={item} className={agent === item ? 'selected' : ''} onClick={() => selectAgent(item)}>{item.toUpperCase()}</button>)}</div>
    <div className="agent-grid">{['recon', 'enum', 'vuln', 'secrets', 'report'].map(name => <AgentStatus key={name} name={name.toUpperCase()} status={stageStatus(workflow.tasks, name)} tasks={workflow.tasks.filter(task => task.task_name.includes(name))} />)}</div>
    {agent === 'overview' && <AttackGraph workflow={workflow} />}
    <div className="operations-grid"><section className="panel"><div className="panel-heading"><h3>{agent.toUpperCase()} TASKS</h3><span className="mono muted">{activeTasks.length} STAGES</span></div>{activeTasks.map(task => {
      const result = resultByTask.get(task.task_name)
      return <article className="scan-task-card" key={task.task_id}><div className="panel-heading"><span className={`status status-${task.status}`}><i />{formatStatus(task.status)}</span><strong>{task.task_name}</strong><small className="mono muted">{task.task_id}</small></div><p className="muted">Retries: {task.retries || 0}{result?.status ? ` · Worker result: ${formatStatus(result.status)}` : ''}</p>{result && <details><summary>Actual worker result</summary><pre className="report-json">{JSON.stringify(result.payload, null, 2)}</pre></details>}</article>
    })}{workflowError && <p className="form-error">{workflowError}</p>}</section><section className="panel terminal-panel"><div className="panel-heading"><h3>LIVE TERMINAL · BACKEND OUTPUT</h3><span className="mono muted">{events.length} EVENTS</span></div><div className="terminal-stream" aria-live="polite">{events.length ? events.map((event, index) => <TerminalEvent key={`${event.task_id || ''}:${event.event || 'event'}:${index}`} event={event} />) : <p className="empty-state">No tool commands or output have been streamed for this scan yet.</p>}</div></section></div>
    <ScanResultsPanel scanId={scan.id} results={results} workflowStatus={workflow.status} taskStatuses={taskStatuses} error={resultsError} />
  </div>
}
function App() {
  const location = useLocation()
  const navigate = useNavigate()
  const [authenticated, setAuthenticated] = useState(Boolean(window.localStorage.getItem('agentsec_token')))
  const [selectedScan, setSelectedScan] = useState(null)
  const [page, setPage] = useState('overview'); const [compact, setCompact] = useState(false); const [data, setData] = useState(EMPTY); const [loading, setLoading] = useState(true); const [error, setError] = useState(''); const [showCreate, setShowCreate] = useState(false); const [attackCatalog, setAttackCatalog] = useState(null); const [attackCatalogError, setAttackCatalogError] = useState(''); const [selectedAttackCategories, setSelectedAttackCategories] = useState([])
  const loadAttackCatalog = async () => {
    setAttackCatalogError('')
    try {
      const value = await api.attackCatalog()
      setAttackCatalog(value.catalog || value)
    } catch (err) {
      setAttackCatalogError(`Unable to load attack catalog: ${err.message}`)
    }
  }
  const load = async (showLoading = true) => { if (showLoading) setLoading(true); try { const [dashboard, scans, findings, reports] = await Promise.all([api.dashboard(), api.scans(), api.findings(), api.reports()]); setData({ dashboard, scans, findings, reports }); setError('') } catch (err) { if (err.status === 401) { window.localStorage.removeItem('agentsec_token'); setAuthenticated(false); setError('Session expired. Sign in again.') } else setError(err.message) } finally { if (showLoading) setLoading(false) } }
  const logout = async () => {
    const refreshToken = window.localStorage.getItem('agentsec_refresh_token')
    try {
      if (refreshToken) await api.logout(refreshToken)
    } catch (err) {
      console.warn('Logout request could not be completed; clearing the local session.', err)
      // Clear the local session even when the server is unavailable.
    } finally {
      window.localStorage.removeItem('agentsec_token')
      window.localStorage.removeItem('agentsec_refresh_token')
      setAuthenticated(false)
      setSelectedScan(null)
      setData(EMPTY)
      setError('')
    }
  }
  useEffect(() => {
    const match = location.pathname.match(/^\/scans\/(\d+)(?:\/([a-z]+))?$/)
    if (!match) { setSelectedScan(null); return }
    const scan = data.scans.find(item => item.id === Number(match[1]))
    if (scan) setSelectedScan(scan)
  }, [location.pathname, data.scans])
  useEffect(() => {
    if (!authenticated) return undefined
    load()
    void loadAttackCatalog()
    return openEventStream(() => {}, err => setError(err.message))
  }, [authenticated])
  useEffect(() => {
    if (!authenticated || !data.scans.some(scan => scan.status === 'queued' || scan.status === 'running')) return undefined
    const poller = window.setInterval(() => load(false), 5000)
    return () => window.clearInterval(poller)
  }, [authenticated, data.scans])
  const titles = useMemo(() => ({ overview: 'COMMAND OVERVIEW', scans: 'SCAN OPERATIONS', git: 'GIT REPOSITORY SCANNING', findings: 'VULNERABILITY INTELLIGENCE', ai: 'AI ANALYSIS STATUS', reports: 'REPORT ARCHIVE', targets: 'TARGET AUTHORIZATION', admin: 'ADMIN AUTHORIZATION REVIEW', postgres: 'POSTGRESQL STATUS' }), [])
  if (!authenticated) return <Login onLogin={() => setAuthenticated(true)} />
  const openScan = (scan) => { setSelectedScan(scan); navigate(`/scans/${scan.id}`) }
  const closeScan = () => { setSelectedScan(null); navigate('/') }
  const navigateToPage = nextPage => { setSelectedScan(null); setPage(nextPage); if (location.pathname.startsWith('/scans/')) navigate('/') }
  return <><div className="app-shell"><Sidebar page={page} setPage={navigateToPage} compact={compact} setCompact={setCompact} onLogout={logout} /><main><Topbar title={selectedScan ? 'LIVE OPERATION CONSOLE' : titles[page]} onRefresh={load} loading={loading} />{error && <div className="error-banner" role="alert"><AlertTriangle size={16} aria-label="Error" />{error}<button className="text-action" onClick={() => load()}>RETRY</button></div>}{selectedScan ? <ScanDetail scan={selectedScan} onBack={closeScan} navigate={navigate} /> : page === 'overview' && <Overview data={data} setPage={navigateToPage} />}{!selectedScan && page === 'scans' && <Scans scans={data.scans} setShowCreate={setShowCreate} catalog={attackCatalog} catalogError={attackCatalogError} onRetry={loadAttackCatalog} selected={selectedAttackCategories} setSelected={setSelectedAttackCategories} onSelect={openScan} />}{!selectedScan && page === 'git' && <GitRepositoryPage scans={data.scans} onScanCreated={scan => { setData(current => ({ ...current, scans: [scan, ...current.scans] })); void load() }} onOpenScan={openScan} />}{!selectedScan && page === 'findings' && <Findings findings={data.findings} />}{!selectedScan && page === 'reports' && <Reports reports={data.reports} />}{!selectedScan && page === 'targets' && <TargetAuthorizationPage />}{!selectedScan && page === 'admin' && <AdminAuthorizationPage />}{!selectedScan && page === 'postgres' && <PostgresStatusPage />}{!selectedScan && page === 'ai' && <AIAnalysisStatusPage />}</main></div>{showCreate && <CreateScan selectedAttackCategories={selectedAttackCategories} onClose={() => setShowCreate(false)} onCreated={scan => { setData(current => ({ ...current, scans: [scan, ...current.scans] })); void load() }} />}</>
}
createRoot(document.getElementById('root')).render(<BrowserRouter><Routes><Route path="*" element={<App />} /></Routes></BrowserRouter>)
