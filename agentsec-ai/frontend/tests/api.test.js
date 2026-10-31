import { afterEach, describe, expect, test, vi } from 'vitest'
import { api } from '../src/api.js'

afterEach(() => vi.restoreAllMocks())

describe('live API client', () => {
  test('loads dashboard details from the backend', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({ ok: true, json: async () => ({ scan_count: 2 }) })
    await expect(api.dashboard()).resolves.toEqual({ scan_count: 2 })
    expect(fetch).toHaveBeenCalledWith('/api/dashboard/details', expect.objectContaining({ headers: expect.any(Object) }))
  })

  test('surfaces backend errors to the UI', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({ ok: false, status: 401, text: async () => 'invalid or expired token' })
    const request = api.scans()
    await expect(request).rejects.toThrow('invalid or expired token')
    await expect(request).rejects.toMatchObject({ status: 401 })
  })

  test('loads scan workflow progress and attributed intel', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue({
      ok: true,
      json: async () => ({ tasks: [], sources: [] }),
    })
    await expect(api.workflow(12)).resolves.toEqual({ tasks: [], sources: [] })
    await expect(api.intelSources()).resolves.toEqual({ tasks: [], sources: [] })
    expect(fetch).toHaveBeenNthCalledWith(1, '/api/scans/12/workflow', expect.any(Object))
    expect(fetch).toHaveBeenNthCalledWith(2, '/api/v1/intel/sources', expect.any(Object))
  })

  test('includes scan id and bearer token in live event socket URL', async () => {
    window.localStorage.setItem('agentsec_token', 'test-token')
    const socket = vi.fn(function Socket() { this.close = vi.fn() })
    vi.stubGlobal('WebSocket', socket)
    const { openEventStream } = await import('../src/api.js')
    openEventStream(() => {}, undefined, 42)
    expect(socket).toHaveBeenCalledWith(expect.stringContaining('/api/ws/events?scan_id=42&token=test-token'))
  })
})
