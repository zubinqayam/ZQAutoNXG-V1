import { useState, useEffect } from 'react';

// Simple API client
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface SystemStatus {
  status: string;
  version: string;
  platform: string;
}

interface Flow {
  id: number;
  name: string;
  description?: string;
}

function App() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [flows, setFlows] = useState<Flow[]>([]);

  useEffect(() => {
    // Check backend health
    fetch(`${API_URL}/health`)
      .then(res => res.json())
      .then(data => setStatus(data))
      .catch(err => console.error("Error connecting to backend:", err));

    // Fetch flows
    fetch(`${API_URL}/flows`)
      .then(res => res.json())
      .then(data => setFlows(data))
      .catch(err => console.error("Error fetching flows:", err));
  }, []);

  return (
    <div className="min-h-screen bg-background text-foreground p-8">
      <header className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight">ZQAutoNXG</h1>
        <p className="text-muted-foreground">Next-Generation Automation Platform</p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="p-6 border rounded-lg shadow-sm bg-card">
          <h2 className="text-xl font-semibold mb-4">System Status</h2>
          {status ? (
            <div className="space-y-2">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Status:</span>
                <span className="font-medium text-green-600">{status.status}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Version:</span>
                <span>{status.version}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Platform:</span>
                <span>{status.platform}</span>
              </div>
            </div>
          ) : (
            <p className="text-yellow-600">Connecting to backend...</p>
          )}
        </div>

        <div className="p-6 border rounded-lg shadow-sm bg-card">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">Recent Flows</h2>
            <button
              className="px-3 py-1 bg-primary text-primary-foreground rounded text-sm hover:opacity-90 transition-opacity"
              onClick={() => alert("Create flow modal would open here")}
            >
              New Flow
            </button>
          </div>

          {flows.length > 0 ? (
            <ul className="space-y-2">
              {flows.map(flow => (
                <li key={flow.id} className="p-3 border rounded hover:bg-accent cursor-pointer transition-colors">
                  <div className="font-medium">{flow.name}</div>
                  <div className="text-sm text-muted-foreground">{flow.description || "No description"}</div>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-muted-foreground italic">No flows found. Create one to get started.</p>
          )}
        </div>
      </div>
    </div>
  )
}

export default App
