import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Activity, CheckCircle2, XCircle, AlertCircle } from "lucide-react";
import { API_URL } from "@/lib/config";

async function getHealth() {
  try {
    const res = await fetch(`${API_URL}/health`, {
      cache: "no-store",
    });
    return await res.json();
  } catch (error) {
    return {
      status: "error",
      message: "Failed to connect to backend",
      timestamp: new Date().toISOString(),
    };
  }
}

function StatusIcon({ status }: { status: string }) {
  switch (status.toLowerCase()) {
    case "healthy":
    case "operational":
      return <CheckCircle2 className="h-6 w-6 text-green-400" />;
    case "degraded":
    case "warning":
      return <AlertCircle className="h-6 w-6 text-yellow-400" />;
    case "error":
    case "unhealthy":
      return <XCircle className="h-6 w-6 text-red-400" />;
    default:
      return <Activity className="h-6 w-6 text-blue-400" />;
  }
}

export default async function HealthPage() {
  const health = await getHealth();

  return (
    <div className="container mx-auto px-4 py-12">
      {/* Header */}
      <div className="mb-8">
        <Link
          href="/"
          className="mb-4 inline-flex items-center gap-2 text-white hover:underline"
        >
          <ArrowLeft className="h-4 w-4" />
          Back to Home
        </Link>
        <h1 className="text-4xl font-bold text-white">
          <Activity className="mb-2 inline-block h-8 w-8" />
          {" "}System Health
        </h1>
        <p className="mt-2 text-white/80">
          Monitor the status of all system components
        </p>
      </div>

      {/* Overall Status */}
      <Card className="mb-6 border-white/20 bg-white/10 backdrop-blur-md">
        <CardHeader>
          <CardTitle className="flex items-center gap-3 text-white">
            <StatusIcon status={health.status} />
            Overall Status
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div>
              <p className="text-sm text-white/70">Status</p>
              <Badge
                variant={
                  health.status === "healthy" || health.status === "operational"
                    ? "success"
                    : "destructive"
                }
                className="mt-1"
              >
                {health.status}
              </Badge>
            </div>
            <div>
              <p className="text-sm text-white/70">Platform</p>
              <p className="text-lg font-semibold text-white">
                {health.platform || "ZQAutoNXG"}
              </p>
            </div>
            <div>
              <p className="text-sm text-white/70">Version</p>
              <p className="text-lg font-semibold text-white">
                {health.version || "6.0.0"}
              </p>
            </div>
          </div>
          {health.timestamp && (
            <div className="mt-4">
              <p className="text-sm text-white/70">Last Updated</p>
              <p className="text-white">
                {new Date(health.timestamp).toLocaleString()}
              </p>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Component Status */}
      {health.components && (
        <div className="mb-6">
          <h2 className="mb-4 text-2xl font-bold text-white">Components</h2>
          <div className="grid gap-4 md:grid-cols-2">
            {Object.entries(health.components).map(([name, status]: [string, any]) => (
              <Card
                key={name}
                className="border-white/20 bg-white/10 backdrop-blur-md"
              >
                <CardHeader>
                  <CardTitle className="flex items-center gap-2 text-white">
                    <StatusIcon status={typeof status === "string" ? status : status.status} />
                    {name}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {typeof status === "string" ? (
                    <Badge
                      variant={
                        status === "healthy" || status === "operational"
                          ? "success"
                          : "destructive"
                      }
                    >
                      {status}
                    </Badge>
                  ) : (
                    <div className="space-y-2 text-sm text-white/80">
                      <div>
                        <strong>Status:</strong>{" "}
                        <Badge
                          variant={
                            status.status === "healthy" || status.status === "operational"
                              ? "success"
                              : "destructive"
                          }
                        >
                          {status.status}
                        </Badge>
                      </div>
                      {status.message && (
                        <div>
                          <strong>Message:</strong> {status.message}
                        </div>
                      )}
                      {status.details && (
                        <div>
                          <strong>Details:</strong>
                          <pre className="mt-1 rounded bg-black/30 p-2 text-xs">
                            {JSON.stringify(status.details, null, 2)}
                          </pre>
                        </div>
                      )}
                    </div>
                  )}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {/* Raw Response */}
      <Card className="border-white/20 bg-white/10 backdrop-blur-md">
        <CardHeader>
          <CardTitle className="text-white">Raw Response</CardTitle>
        </CardHeader>
        <CardContent>
          <pre className="overflow-x-auto rounded bg-black/50 p-4 text-xs text-white">
            {JSON.stringify(health, null, 2)}
          </pre>
        </CardContent>
      </Card>

      {/* Footer */}
      <footer className="mt-12 text-center text-white/70">
        <p className="text-sm">
          ZQAutoNXG v6.0.0 — Powered by ZQ AI LOGIC™
        </p>
      </footer>
    </div>
  );
}
