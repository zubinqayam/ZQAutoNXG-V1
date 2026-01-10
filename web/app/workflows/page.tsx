import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Activity, Plus } from "lucide-react";

async function getWorkflows() {
  try {
    const res = await fetch("http://localhost:8000/api/v1/workflows", {
      cache: "no-store",
    });
    if (res.ok) {
      return await res.json();
    }
    return [];
  } catch (error) {
    console.error("Failed to fetch workflows:", error);
    return [];
  }
}

export default async function WorkflowsPage() {
  const workflows = await getWorkflows();

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
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold text-white">
              <Activity className="mb-2 inline-block h-8 w-8" />
              {" "}Workflows
            </h1>
            <p className="mt-2 text-white/80">
              Manage and monitor your automation workflows
            </p>
          </div>
          <button className="inline-flex items-center gap-2 rounded-lg bg-white px-6 py-3 font-medium text-primary-600 transition-colors hover:bg-white/90">
            <Plus className="h-5 w-5" />
            Create Workflow
          </button>
        </div>
      </div>

      {/* Workflows Grid */}
      {workflows.length === 0 ? (
        <Card className="border-white/20 bg-white/10 backdrop-blur-md">
          <CardContent className="py-12 text-center">
            <Activity className="mx-auto mb-4 h-12 w-12 text-white/50" />
            <h3 className="mb-2 text-xl font-semibold text-white">
              No workflows yet
            </h3>
            <p className="text-white/70">
              Create your first workflow to get started with automation
            </p>
            <button className="mt-6 inline-flex items-center gap-2 rounded-lg bg-white px-6 py-3 font-medium text-primary-600 transition-colors hover:bg-white/90">
              <Plus className="h-5 w-5" />
              Create First Workflow
            </button>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
          {workflows.map((workflow: any) => (
            <Card
              key={workflow.id}
              className="border-white/20 bg-white/10 backdrop-blur-md transition-all hover:bg-white/15"
            >
              <CardHeader>
                <div className="flex items-start justify-between">
                  <CardTitle className="text-xl text-white">
                    {workflow.name || "Untitled Workflow"}
                  </CardTitle>
                  <Badge variant="secondary">
                    {workflow.status || "active"}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 text-sm text-white/80">
                  <div>
                    <strong>ID:</strong> {workflow.id}
                  </div>
                  {workflow.description && (
                    <div>
                      <strong>Description:</strong> {workflow.description}
                    </div>
                  )}
                  <div>
                    <strong>Nodes:</strong> {workflow.nodes?.length || 0}
                  </div>
                  <div>
                    <strong>Edges:</strong> {workflow.edges?.length || 0}
                  </div>
                </div>
                <div className="mt-4 flex gap-2">
                  <Link
                    href={`/workflows/${workflow.id}`}
                    className="flex-1 rounded-lg border-2 border-white px-4 py-2 text-center text-sm font-medium text-white transition-colors hover:bg-white/10"
                  >
                    View Details
                  </Link>
                  <button className="flex-1 rounded-lg bg-primary-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-primary-600">
                    Edit
                  </button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Footer */}
      <footer className="mt-12 text-center text-white/70">
        <p className="text-sm">
          ZQAutoNXG v6.0.0 — Powered by ZQ AI LOGIC™
        </p>
      </footer>
    </div>
  );
}
