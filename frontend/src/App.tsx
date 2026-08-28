import { FormEvent, useEffect, useMemo, useState } from 'react'

const API_URL = (import.meta.env.VITE_API_URL || 'http://localhost:8000').replace(/\/$/, '')

type Health = {
  status: string
  platform: string
  version: string
}

type Workflow = {
  id: string
  name: string
  description?: string | null
  status?: string
  nodes?: unknown[]
  edges?: unknown[]
}

type LogEntry = {
  timestamp: string
  level: string
  message: string
  metadata?: Record<string, unknown>
}

type TopologyNode = {
  id: string
  label: string
  status: string
  type: string
  metrics?: Record<string, unknown>
}

type Topology = {
  nodes: TopologyNode[]
  connections: Array<{ id: string; source: string; target: string; status: string }>
  timestamp: string
}

type SystemStatus = {
  status: string
  architecture: string
  uptime_seconds: number
  components: Record<string, { status: string; message?: string }>
  integrations: Record<string, { status: string; message?: string }>
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, init)
  if (!response.ok) {
    const body = await response.text()
    throw new Error(`${response.status} ${response.statusText}${body ? `: ${body}` : ''}`)
  }
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

function statusClass(status = 'unknown') {
  const normalized = status.toLowerCase()
  if (['healthy', 'ready', 'active', 'enabled', 'published', 'success'].includes(normalized)) {
    return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
  }
  if (['degraded', 'warn', 'warning'].includes(normalized)) {
    return 'bg-amber-500/10 text-amber-300 border-amber-500/30'
  }
  if (['error', 'failed', 'unhealthy', 'unavailable'].includes(normalized)) {
    return 'bg-red-500/10 text-red-300 border-red-500/30'
  }
  return 'bg-slate-500/10 text-slate-300 border-slate-500/30'
}

function Badge({ value }: { value?: string }) {
  return (
    <span className={`inline-flex rounded-full border px-2 py-0.5 text-xs font-medium ${statusClass(value)}`}>
      {value || 'unknown'}
    </span>
  )
}

function App() {
  const [health, setHealth] = useState<Health | null>(null)
  const [system, setSystem] = useState<SystemStatus | null>(null)
  const [workflows, setWorkflows] = useState<Workflow[]>([])
  const [nodeStatuses, setNodeStatuses] = useState<Record<string, string>>({})
  const [topology, setTopology] = useState<Topology | null>(null)
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState<string | null>(null)

  const load = async () => {
    try {
      const [healthData, statusData, workflowData, nodeData, topologyData, logData] = await Promise.all([
        request<Health>('/health'),
        request<SystemStatus>('/status'),
        request<Workflow[]>('/api/v1/workflows'),
        request<Record<string, string>>('/api/v1/nodes/status'),
        request<Topology>('/api/v1/network/topology'),
        request<LogEntry[]>('/api/v1/logs/history?limit=20'),
      ])
      setHealth(healthData)
      setSystem(statusData)
      setWorkflows(workflowData)
      setNodeStatuses(nodeData)
      setTopology(topologyData)
      setLogs(logData)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to load ZQAutoNXG')
    }
  }

  useEffect(() => {
    void load()
    const timer = window.setInterval(() => void load(), 15000)

    const wsBase = API_URL.replace(/^http/, 'ws')
    const socket = new WebSocket(`${wsBase}/api/v1/logs/ws`)
    socket.onmessage = (event) => {
      try {
        const entry = JSON.parse(event.data) as LogEntry
        if (entry.timestamp && entry.level && entry.message) {
          setLogs((current) => [...current.slice(-19), entry])
        }
      } catch {
        // Ignore heartbeat/non-log frames.
      }
    }

    return () => {
      window.clearInterval(timer)
      socket.close()
    }
  }, [])

  const componentSummary = useMemo(() => {
    if (!system) return []
    return Object.entries(system.components)
  }, [system])

  const createWorkflow = async (event: FormEvent) => {
    event.preventDefault()
    if (!name.trim()) return
    setBusy('create')
    try {
      await request<Workflow>('/api/v1/workflows', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: name.trim(),
          description: description.trim() || null,
          nodes: [],
          edges: [],
        }),
      })
      setName('')
      setDescription('')
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unable to create workflow')
    } finally {
      setBusy(null)
    }
  }

  const workflowAction = async (workflow: Workflow, action: 'execute' | 'activate' | 'delete') => {
    setBusy(`${action}:${workflow.id}`)
    try {
      if (action === 'delete') {
        await request<void>(`/api/v1/workflows/${workflow.id}`, { method: 'DELETE' })
      } else {
        await request(`/api/v1/workflows/${action}?workflow_id=${encodeURIComponent(workflow.id)}`, {
          method: 'POST',
        })
      }
      await load()
    } catch (err) {
      setError(err instanceof Error ? err.message : `Unable to ${action} workflow`)
    } finally {
      setBusy(null)
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto max-w-7xl space-y-6 p-4 md:p-8">
        <header className="flex flex-col gap-4 border-b border-slate-800 pb-6 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.28em] text-cyan-400">ZQ AI LOGIC</p>
            <h1 className="mt-2 text-3xl font-bold tracking-tight md:text-4xl">ZQAutoNXG Control Plane</h1>
            <p className="mt-2 max-w-2xl text-sm text-slate-400">
              Workflows, node state, live logs, network topology, health and deployment telemetry from one runtime.
            </p>
          </div>
          <div className="flex items-center gap-3">
            <Badge value={health?.status || (error ? 'unhealthy' : 'loading')} />
            <span className="text-sm text-slate-400">v{health?.version || '—'}</span>
          </div>
        </header>

        {error && (
          <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-sm text-red-200">
            {error}
          </div>
        )}

        <section className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
          <Metric label="Runtime" value={system?.status || 'loading'} />
          <Metric label="Architecture" value={system?.architecture || 'G V2 NovaBase'} />
          <Metric label="Workflows" value={String(workflows.length)} />
          <Metric label="Topology nodes" value={String(topology?.nodes?.length || 0)} />
        </section>

        <section className="grid gap-6 lg:grid-cols-[1.4fr_1fr]">
          <Panel title="Workflow operations" subtitle="Create, execute, activate and retire workflows through the enterprise API.">
            <form onSubmit={createWorkflow} className="mb-5 grid gap-3 rounded-xl border border-slate-800 bg-slate-900/50 p-4 md:grid-cols-[1fr_1.5fr_auto]">
              <input
                value={name}
                onChange={(event) => setName(event.target.value)}
                placeholder="Workflow name"
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm outline-none focus:border-cyan-500"
              />
              <input
                value={description}
                onChange={(event) => setDescription(event.target.value)}
                placeholder="Description"
                className="rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-sm outline-none focus:border-cyan-500"
              />
              <button
                type="submit"
                disabled={busy === 'create' || !name.trim()}
                className="rounded-lg bg-cyan-500 px-4 py-2 text-sm font-semibold text-slate-950 disabled:cursor-not-allowed disabled:opacity-50"
              >
                Create
              </button>
            </form>

            <div className="space-y-3">
              {workflows.length === 0 ? (
                <Empty text="No workflows yet. Create the first workflow above." />
              ) : (
                workflows.map((workflow) => (
                  <div key={workflow.id} className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
                    <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="font-semibold">{workflow.name}</h3>
                          <Badge value={workflow.status || 'draft'} />
                        </div>
                        <p className="mt-1 text-sm text-slate-400">{workflow.description || 'No description'}</p>
                        <p className="mt-2 text-xs text-slate-500">
                          {workflow.nodes?.length || 0} nodes · {workflow.edges?.length || 0} edges
                        </p>
                      </div>
                      <div className="flex flex-wrap gap-2">
                        <ActionButton label="Execute" onClick={() => void workflowAction(workflow, 'execute')} disabled={busy !== null} />
                        <ActionButton label="Activate" onClick={() => void workflowAction(workflow, 'activate')} disabled={busy !== null} />
                        <ActionButton label="Delete" onClick={() => void workflowAction(workflow, 'delete')} disabled={busy !== null} danger />
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          </Panel>

          <Panel title="Runtime components" subtitle="Current readiness declarations and integration state.">
            <div className="space-y-3">
              {componentSummary.map(([key, component]) => (
                <div key={key} className="flex items-start justify-between gap-3 rounded-lg border border-slate-800 p-3">
                  <div>
                    <p className="text-sm font-medium">{key.replaceAll('_', ' ')}</p>
                    {component.message && <p className="mt-1 text-xs text-slate-500">{component.message}</p>}
                  </div>
                  <Badge value={component.status} />
                </div>
              ))}
              {system && Object.entries(system.integrations).map(([key, integration]) => (
                <div key={key} className="flex items-start justify-between gap-3 rounded-lg border border-slate-800 p-3">
                  <div>
                    <p className="text-sm font-medium">{key.replaceAll('_', ' ')}</p>
                    {integration.message && <p className="mt-1 text-xs text-slate-500">{integration.message}</p>}
                  </div>
                  <Badge value={integration.status} />
                </div>
              ))}
            </div>
          </Panel>
        </section>

        <section className="grid gap-6 lg:grid-cols-2">
          <Panel title="Network topology" subtitle="Current bridge topology and health state.">
            <div className="grid gap-3 sm:grid-cols-2">
              {topology?.nodes?.map((node) => (
                <div key={node.id} className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
                  <div className="flex items-center justify-between gap-2">
                    <p className="font-medium">{node.label}</p>
                    <Badge value={node.status} />
                  </div>
                  <p className="mt-1 text-xs uppercase tracking-wider text-slate-500">{node.type}</p>
                  {node.metrics && (
                    <div className="mt-3 text-xs text-slate-400">
                      {Object.entries(node.metrics).slice(0, 3).map(([key, value]) => (
                        <span key={key} className="mr-3 inline-block">{key.replaceAll('_', ' ')}: {String(value)}</span>
                      ))}
                    </div>
                  )}
                </div>
              )) || <Empty text="Topology unavailable." />}
            </div>
          </Panel>

          <Panel title="Live activity" subtitle="Bounded log history plus WebSocket updates.">
            <div className="max-h-[420px] space-y-2 overflow-auto font-mono text-xs">
              {logs.length === 0 ? (
                <Empty text="No log entries yet. Live entries appear when the console is connected." />
              ) : (
                [...logs].reverse().map((entry, index) => (
                  <div key={`${entry.timestamp}-${index}`} className="rounded-lg border border-slate-800 bg-slate-950/60 p-3">
                    <div className="flex items-center justify-between gap-3">
                      <Badge value={entry.level} />
                      <span className="text-slate-600">{new Date(entry.timestamp).toLocaleTimeString()}</span>
                    </div>
                    <p className="mt-2 text-slate-300">{entry.message}</p>
                  </div>
                ))
              )}
            </div>
          </Panel>
        </section>

        <section>
          <Panel title="Node registry" subtitle="Node enablement state reported by the runtime.">
            {Object.keys(nodeStatuses).length === 0 ? (
              <Empty text="No configured nodes are registered yet." />
            ) : (
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                {Object.entries(nodeStatuses).map(([id, status]) => (
                  <div key={id} className="flex items-center justify-between rounded-lg border border-slate-800 p-3">
                    <span className="truncate text-sm text-slate-300">{id}</span>
                    <Badge value={status} />
                  </div>
                ))}
              </div>
            )}
          </Panel>
        </section>
      </div>
    </main>
  )
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-4">
      <p className="text-xs uppercase tracking-wider text-slate-500">{label}</p>
      <p className="mt-2 truncate text-xl font-semibold text-slate-100">{value}</p>
    </div>
  )
}

function Panel({ title, subtitle, children }: { title: string; subtitle: string; children: React.ReactNode }) {
  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900/25 p-4 md:p-5">
      <div className="mb-4">
        <h2 className="text-lg font-semibold">{title}</h2>
        <p className="mt-1 text-sm text-slate-500">{subtitle}</p>
      </div>
      {children}
    </section>
  )
}

function ActionButton({ label, onClick, disabled, danger = false }: { label: string; onClick: () => void; disabled: boolean; danger?: boolean }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`rounded-lg border px-3 py-1.5 text-xs font-medium disabled:cursor-not-allowed disabled:opacity-50 ${
        danger
          ? 'border-red-500/30 text-red-300 hover:bg-red-500/10'
          : 'border-slate-700 text-slate-200 hover:border-cyan-500/50 hover:bg-cyan-500/5'
      }`}
    >
      {label}
    </button>
  )
}

function Empty({ text }: { text: string }) {
  return <p className="rounded-lg border border-dashed border-slate-800 p-4 text-sm text-slate-500">{text}</p>
}

export default App
