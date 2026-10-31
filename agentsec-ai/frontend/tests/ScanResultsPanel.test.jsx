// @vitest-environment jsdom
import { afterEach, describe, expect, it, vi } from 'vitest'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import ScanResultsPanel from '../src/components/scans/ScanResultsPanel'
import { downloadCsv, downloadJson } from '../src/api'

vi.mock('../src/api', () => ({
  downloadCsv: vi.fn(),
  downloadJson: vi.fn(),
}))

afterEach(() => cleanup())

describe('ScanResultsPanel', () => {
  it('distinguishes a running scan with no returned results', () => {
    render(<ScanResultsPanel scanId={7} results={[]} workflowStatus="running" taskStatuses={['running']} />)

    expect(screen.getByText('Workers are still running. No result has been returned yet.')).toBeTruthy()
    expect(screen.queryByText(/example\.com/i)).toBeNull()
  })

  it('shows verified structured output and expandable raw payload', () => {
    const result = {
      scan_id: 7,
      task_id: 'celery-task-7',
      tool_name: 'workers.enum.run',
      status: 'SUCCESS',
      payload: { live_hosts: 1, tools: [{ tool: 'httpx_plugin', success: true, results: [{ url: 'https://authorized.test' }] }] },
    }
    render(<ScanResultsPanel scanId={7} results={[result]} workflowStatus="completed" taskStatuses={['completed']} />)

    expect(screen.getByText('WORKER RESULTS')).toBeTruthy()
    expect(screen.getByText(/Verified against scan #7 and Celery task celery-task-7/)).toBeTruthy()
    fireEvent.click(screen.getByText('JSON'))
    fireEvent.click(screen.getByText('CSV'))
    expect(downloadJson).toHaveBeenCalledWith('scan-7-results.json', [result])
    expect(downloadCsv).toHaveBeenCalledWith('scan-7-results.csv', [result])
    fireEvent.click(screen.getByText('httpx_plugin'))
    expect(screen.getAllByText(/"url": "https:\/\/authorized\.test"/)).toHaveLength(2)
    fireEvent.click(screen.getByText('Expand verified worker return'))
    expect(screen.getByText(/"live_hosts": 1/)).toBeTruthy()
  })

  it('explains failed scans without inventing output', () => {
    render(<ScanResultsPanel scanId={8} results={[]} workflowStatus="failed" taskStatuses={['failed']} />)

    expect(screen.getByText(/scan failed before a verified worker result was persisted/i)).toBeTruthy()
  })
})
