import Link from "next/link";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Rocket, Sparkles, Globe, Shield, Activity } from "lucide-react";

async function getStatus() {
  try {
    const res = await fetch("http://localhost:8000/", {
      cache: "no-store",
    });
    return await res.json();
  } catch (error) {
    return {
      platform: "ZQAutoNXG",
      version: "6.0.0",
      status: "connecting",
    };
  }
}

export default async function HomePage() {
  const status = await getStatus();

  return (
    <div className="container mx-auto px-4 py-12">
      {/* Header */}
      <div className="mb-12 text-center">
        <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-white/10 px-4 py-2 backdrop-blur-sm">
          <Sparkles className="h-4 w-4 text-yellow-300" />
          <span className="text-sm font-medium text-white">
            Powered by ZQ AI LOGIC™
          </span>
        </div>
        <h1 className="mb-4 text-6xl font-bold text-white">
          <Rocket className="mb-2 inline-block h-12 w-12" />
          <br />
          ZQAutoNXG
        </h1>
        <p className="mx-auto max-w-2xl text-xl text-white/90">
          Next-Generation eXtended Automation Platform
        </p>
        <div className="mt-6 flex flex-wrap items-center justify-center gap-2">
          <Badge variant="secondary">v{status.version}</Badge>
          <Badge variant={status.status === "operational" ? "success" : "default"}>
            {status.status}
          </Badge>
          <Badge variant="outline" className="text-white">
            {status.architecture || "G V2 NovaBase"}
          </Badge>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card className="border-white/20 bg-white/10 backdrop-blur-md">
          <div className="p-6">
            <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-primary-500">
              <Activity className="h-6 w-6 text-white" />
            </div>
            <h3 className="mb-2 text-xl font-semibold text-white">
              AI-Powered Automation
            </h3>
            <p className="text-white/80">
              Intelligent workflow generation and optimization using proprietary
              algorithms
            </p>
            <Link
              href="/workflows"
              className="mt-4 inline-block text-sm font-medium text-white hover:underline"
            >
              View Workflows →
            </Link>
          </div>
        </Card>

        <Card className="border-white/20 bg-white/10 backdrop-blur-md">
          <div className="p-6">
            <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-purple-500">
              <Globe className="h-6 w-6 text-white" />
            </div>
            <h3 className="mb-2 text-xl font-semibold text-white">
              Global-Scale Orchestration
            </h3>
            <p className="text-white/80">
              Distributed deployment and management across multiple regions
            </p>
            <Link
              href="/nodes"
              className="mt-4 inline-block text-sm font-medium text-white hover:underline"
            >
              Manage Nodes →
            </Link>
          </div>
        </Card>

        <Card className="border-white/20 bg-white/10 backdrop-blur-md">
          <div className="p-6">
            <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-green-500">
              <Shield className="h-6 w-6 text-white" />
            </div>
            <h3 className="mb-2 text-xl font-semibold text-white">
              Enterprise Security
            </h3>
            <p className="text-white/80">
              Apache 2.0 licensed with comprehensive security monitoring
            </p>
            <Link
              href="/health"
              className="mt-4 inline-block text-sm font-medium text-white hover:underline"
            >
              System Health →
            </Link>
          </div>
        </Card>
      </div>

      {/* Quick Actions */}
      <div className="mt-12">
        <Card className="border-white/20 bg-white/10 backdrop-blur-md">
          <div className="p-8 text-center">
            <h2 className="mb-4 text-2xl font-bold text-white">Get Started</h2>
            <div className="flex flex-wrap justify-center gap-4">
              <Link
                href="/docs"
                className="inline-flex items-center gap-2 rounded-lg bg-white px-6 py-3 font-medium text-primary-600 transition-colors hover:bg-white/90"
              >
                📚 Documentation
              </Link>
              <Link
                href="/api"
                className="inline-flex items-center gap-2 rounded-lg border-2 border-white px-6 py-3 font-medium text-white transition-colors hover:bg-white/10"
              >
                🔌 API Reference
              </Link>
              <a
                href="http://localhost:8000/docs"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-lg border-2 border-white px-6 py-3 font-medium text-white transition-colors hover:bg-white/10"
              >
                📊 Backend API
              </a>
            </div>
          </div>
        </Card>
      </div>

      {/* Footer */}
      <footer className="mt-12 text-center text-white/80">
        <p className="text-sm">
          Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC™
        </p>
        <p className="mt-2 text-xs">
          Licensed under the Apache License 2.0
        </p>
      </footer>
    </div>
  );
}
