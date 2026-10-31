import { downloadCsv, downloadJson, downloadSarif } from '../../api'

function ResultSummary({ payload }) {
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) return null
  const values = [
    ['Discovered', payload.discovered_count],
    ['Findings', payload.total_findings],
    ['Live hosts', payload.live_hosts],
    ['Open ports', payload.open_ports],
    ['Endpoints', payload.endpoint_count],
  ].filter(([, value]) => value !== undefined)
  if (!values.length) return null
  return <div className="result-summary">{values.map(([label, value]) => <span key={label}><small>{label}</small><strong>{value}</strong></span>)}</div>
}

function ErrorSummary({ payload }) {
  if (!payload || typeof payload !== 'object' || Array.isArray(payload)) return null
  const errors = [
    ...(Array.isArray(payload.tool_errors) ? payload.tool_errors : []),
    ...(Array.isArray(payload.tools) ? payload.tools.filter(tool => tool.success === false).map(tool => ({
      tool: tool.tool,
      error: tool.error || 'Tool execution failed',
    })) : []),
  ]
  if (!errors.length) return null
  return <div className="result-errors"><strong>Tool errors</strong>{errors.map((item, index) => <p key={`${item.tool || 'error'}-${index}`}><b>{item.tool || item.plugin || 'Tool'}:</b> {item.error || 'Tool execution failed'}</p>)}</div>
}

function StructuredToolResults({ payload }) {
  if (!payload || typeof payload !== 'object' || !Array.isArray(payload.tools)) return null
  return <div className="result-tool-list">{payload.tools.map((tool, index) => {
    const records = tool.results ?? tool.parsed ?? []
    const recordCount = tool.record_count ?? (Array.isArray(records) ? records.length : 0)
    return <details className="result-tool" key={`${tool.tool || tool.plugin || 'tool'}-${index}`}>
      <summary><strong>{tool.tool || tool.plugin || 'Tool output'}</strong><span>{tool.success === false ? 'FAILED' : `${recordCount} RECORDS`}</span></summary>
      <pre>{JSON.stringify(records, null, 2)}</pre>
    </details>
  })}</div>
}

export default function ScanResultsPanel({ scanId, results, workflowStatus, taskStatuses, error }) {
  const noResultMessage = error
    ? `Unable to load this scan's results: ${error}`
    : workflowStatus === 'failed'
      ? 'The scan failed before a verified worker result was persisted. Check the task states and terminal output.'
      : workflowStatus === 'queued' || workflowStatus === 'running' || taskStatuses.some(status => status === 'queued' || status === 'running' || status === 'retrying')
        ? 'Workers are still running. No result has been returned yet.'
        : 'No verified worker results were returned for this scan.'

  return <section className="panel scan-results-panel">
    <div className="panel-heading">
      <div><span className="eyebrow">SCAN #{scanId}</span><h3>WORKER RESULTS</h3></div>
      {results.length > 0 && <div className="result-export-actions">
        <button className="text-action" onClick={() => downloadJson(`scan-${scanId}-results.json`, results)}>JSON</button>
        <button className="text-action" onClick={() => downloadCsv(`scan-${scanId}-results.csv`, results)}>CSV</button>
        <button className="text-action" onClick={() => downloadSarif(`scan-${scanId}-results.sarif`, results)}>SARIF</button>
      </div>}
    </div>
    {results.length === 0 ? <p className="empty-state result-empty">{noResultMessage}</p> : <div className="scan-result-list">
      {results.map(result => <article className="scan-result" key={`${result.task_id}:${result.tool_name}`}>
        <div className="scan-result-heading">
          <div><strong>{result.tool_name}</strong><span className="mono muted">TASK {result.task_id}</span></div>
          <span className={`result-status result-status-${result.status.toLowerCase()}`}>{result.status}</span>
        </div>
        <ResultSummary payload={result.payload} />
        <StructuredToolResults payload={result.payload} />
        {typeof result.payload === 'string' && result.status !== 'SUCCESS' && <pre className="result-error-output">{result.payload}</pre>}
        <ErrorSummary payload={result.payload} />
        <details className="result-raw">
          <summary>Expand verified worker return</summary>
          <pre>{JSON.stringify(result.payload, null, 2)}</pre>
        </details>
        <small className="result-provenance">Verified against scan #{result.scan_id} and Celery task {result.task_id}</small>
      </article>)}
    </div>}
  </section>
}
