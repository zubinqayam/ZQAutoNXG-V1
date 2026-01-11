# ZQAutoNXG Frontend

**Version:** 6.0.0 (Minimal Web Interface)  
**Status:** Basic HTML/JavaScript interface with Vercel Web Analytics

## Overview

This is a minimal web interface for the ZQAutoNXG platform. It provides basic interaction capabilities with the backend API and includes integrated Vercel Web Analytics for tracking user interactions.

## Features

- Platform status monitoring
- Workflow creation and viewing
- Activity logs display
- Quick access to API documentation
- Real-time status updates
- **Vercel Web Analytics integration** for tracking user behavior

## Vercel Web Analytics

The frontend includes Vercel Web Analytics for privacy-preserving analytics. The following events are automatically tracked:

- **Page Views**: Tracks when users visit the UI
- **Workflow Creation**: Tracks when new workflows are created
- **Workflow Viewing**: Tracks when workflows are viewed

### Setup

See [VERCEL_ANALYTICS_SETUP.md](/VERCEL_ANALYTICS_SETUP.md) in the repository root for complete setup instructions.

Quick summary:
1. Enable Web Analytics in your Vercel dashboard
2. Run `npm install` to install the analytics package
3. Deploy to Vercel using `vercel deploy`
4. View analytics in your Vercel dashboard

## Usage

### Via Backend Server

The frontend is automatically served by the backend at `/ui`:

```bash
# Start backend
cd ..
uvicorn zqautonxg.app:app --host 0.0.0.0 --port 8000

# Access UI
# Open browser to: http://localhost:8000/ui
```

### Standalone

You can also open the HTML file directly:

```bash
# Open in browser
open index.html  # macOS
xdg-open index.html  # Linux
start index.html  # Windows
```

## Dependencies

The frontend includes the following npm dependencies:

- `@vercel/analytics@^1.4.0` - Vercel Web Analytics tracking

Install dependencies with:

```bash
npm install
# or
pnpm install
# or
yarn install
# or
bun install
```

## API Integration

The interface connects to the backend API at:
- Base URL: `http://localhost:8000`
- Workflows: `/api/v1/workflows`
- Nodes: `/api/v1/nodes`
- Logs: `/api/v1/logs`
- Network: `/api/v1/network`

## Future Enhancements

This is a minimal interface. The full React + TypeScript frontend with advanced features will be implemented in future versions:

- Drag-and-drop workflow designer with React Flow
- Real-time log streaming with WebSocket
- Network topology visualization
- Node configuration panels
- OAuth configuration wizard
- Advanced monitoring dashboards
- Advanced Vercel Analytics dashboard with custom filters

## Contributing

See the main [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for guidelines.

---

**Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC™**  
**Licensed under the Apache License 2.0**

