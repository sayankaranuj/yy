const API_ROOT = import.meta.env.VITE_API_ROOT || '/api'

async function request(path, options = {}) {
  const token = window.localStorage.getItem('agentsec_token')
  const controller = new AbortController()
  const timeout = window.setTimeout(() => controller.abort(), 15000)
  let response
  try {
    response = await fetch(`${API_ROOT}${path}`, {
      ...options,
      signal: options.signal || controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...(options.headers || {}),
      },
    })
  } catch (error) {
    if (error.name === 'AbortError') throw new Error('Backend request timed out. Check that the API service is running.')
    throw error
  } finally {
    window.clearTimeout(timeout)
  }
  if (!response.ok) {
    const body = await response.text()
    let detail = body || `Request failed: ${response.status}`
    try {
      const parsed = JSON.parse(body)
      if (Array.isArray(parsed.detail)) {
        detail = parsed.detail.map(item => item.msg || 'Invalid request').join('; ')
      } else {
        detail = parsed.detail || parsed.message || detail
      }
    } catch {
      // Keep the plain-text response when the backend did not return JSON.
    }
    const error = new Error(detail)
    error.status = response.status
    throw error
  }
  return response.status === 204 ? null : response.json()
}

export const api = {
  login: (payload) => request('/auth/login', { method: 'POST', body: JSON.stringify(payload) }),
  logout: (refreshToken) => request('/auth/logout', {
    method: 'POST',
    body: JSON.stringify({ refresh_token: refreshToken }),
  }),
  aiStatus: () => request('/ai/status'),
  databaseStatus: () => request('/database/status'),
  dashboard: () => request('/dashboard/details'),
  scans: () => request('/scans'),
  attackCatalog: () => request('/scans/attack-catalog'),
  intelSources: () => request('/v1/intel/sources'),
  intelSample: (category, count = 20) => request(`/v1/intel/sample/${category}?count=${count}`),
  createScan: (payload) => request('/scans', { method: 'POST', body: JSON.stringify(payload) }),
  cancelScan: (scanId) => request(`/scans/${scanId}/cancel`, { method: 'POST' }),
  resumeScan: (scanId) => request(`/scans/${scanId}/resume`, { method: 'POST' }),
  workflow: (scanId) => request(`/scans/${scanId}/workflow`),
  scanResults: (scanId) => request(`/scans/${scanId}/results`),
  findings: () => request('/findings'),
  reports: () => request('/reports'),
  report: (scanId) => request(`/reports/${scanId}`),
  targets: () => request('/targets'),
  authorizationRequests: () => request('/targets/requests'),
  createAuthorizationRequest: (payload) => request('/targets/requests', { method: 'POST', body: JSON.stringify(payload) }),
  reviewAuthorizationRequest: (requestId, payload) => request(`/targets/requests/${requestId}/decision`, { method: 'POST', body: JSON.stringify(payload) }),
  createTargetVerification: (payload) => request('/targets/verification', { method: 'POST', body: JSON.stringify(payload) }),
  verifyTarget: (payload) => request('/targets/verification/verify', { method: 'POST', body: JSON.stringify(payload) }),
  approveTarget: (payload) => request('/targets', { method: 'POST', body: JSON.stringify(payload) }),
  revokeTarget: (target) => request(`/targets/${encodeURIComponent(target)}`, { method: 'DELETE' }),
}

export function openEventStream(onEvent, onError, scanId = null) {
  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
  const params = new URLSearchParams()
  if (scanId) params.set('scan_id', scanId)
  const token = window.localStorage.getItem('agentsec_token')
  if (token) params.set('token', token)
  const suffix = params.toString() ? `?${params.toString()}` : ''
  let socket
  let stopped = false
  let reconnectTimer
  const connect = () => {
    if (stopped) return
    socket = new WebSocket(`${protocol}//${window.location.host}${API_ROOT}/ws/events${suffix}`)
    socket.onmessage = (message) => {
      try { onEvent(JSON.parse(message.data)) } catch { onError?.(new Error('Invalid event payload')) }
    }
    socket.onerror = () => onError?.(new Error('Live event stream unavailable; retrying.'))
    socket.onclose = () => {
      if (!stopped) reconnectTimer = window.setTimeout(connect, 3000)
    }
  }
  connect()
  return () => {
    stopped = true
    window.clearTimeout(reconnectTimer)
    socket?.close()
  }
}

export function downloadJson(name, payload) {
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = name
  anchor.click()
  URL.revokeObjectURL(url)
}

export function downloadCsv(name, rows) {
  const columns = ['scan_id', 'task_id', 'tool_name', 'status', 'payload']
  const escape = (value) => {
    const text = typeof value === 'string' ? value : JSON.stringify(value ?? '')
    return `"${text.replaceAll('"', '""')}"`
  }

  const contents = [
    columns.join(','),
    ...rows.map(row => columns.map(column => escape(row[column])).join(',')),
  ].join('\r\n')
  const blob = new Blob([contents], { type: 'text/csv;charset=utf-8' })
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = name
  anchor.click()
  URL.revokeObjectURL(url)
}

export function downloadSarif(name, results) {
  const sarif = {
    version: '2.1.0',
    $schema: 'https://json.schemastore.org/sarif-2.1.0.json',
    runs: results.map(result => ({
      tool: { driver: { name: result.tool_name || 'FOUND FIRST worker' } },
      results: (result.payload?.findings || []).map(finding => ({
        ruleId: finding.DetectorName || finding.detector || 'secret',
        level: result.status === 'FAILED' ? 'error' : 'warning',
        message: { text: finding.description || 'Finding returned by the scanner.' },
        locations: [{ physicalLocation: { artifactLocation: { uri: finding.SourceMetadata?.Data?.Git?.link || 'repository' } } }],
      })),
    })),
  }
  downloadJson(name, sarif)
}

export async function downloadPdf(name, path) {
  const token = window.localStorage.getItem('agentsec_token')
  const response = await fetch(`${API_ROOT}${path}`, {
    headers: token ? { Authorization: `Bearer ${token}` } : {},
  })
  if (!response.ok) throw new Error(`PDF export failed: ${response.status}`)
  const blob = await response.blob()
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = name
  anchor.click()
  URL.revokeObjectURL(url)
}
