# ZQAutoNXG Frontend

**Version:** 6.0.0 (Minimal Web Interface)  
**Status:** Basic HTML/JavaScript interface

## Overview

This is a minimal web interface for the ZQAutoNXG platform. It provides basic interaction capabilities with the backend API.

## Features

- Platform status monitoring
- Workflow creation and viewing
- Activity logs display
- Quick access to API documentation
- Real-time status updates
- Vercel Web Analytics integration for tracking visitor metrics

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

## API Integration

The interface connects to the backend API at:
- Base URL: `http://localhost:8000`
- Workflows: `/api/v1/workflows`
- Nodes: `/api/v1/nodes`
- Logs: `/api/v1/logs`
- Network: `/api/v1/network`

## Analytics

The frontend includes Vercel Web Analytics integration to track visitor metrics and page views. When deployed to Vercel, analytics data will be automatically collected at the `/_vercel/insights/*` routes.

To enable analytics in your Vercel project:
1. Navigate to your project dashboard on Vercel
2. Click on the **Analytics** tab
3. Click **Enable** to activate Web Analytics
4. Deploy your application - analytics will start tracking automatically

No additional configuration is needed as the analytics script is already integrated into the HTML file.

## Future Enhancements

This is a minimal interface. The full React + TypeScript frontend with advanced features will be implemented in future versions:

- Drag-and-drop workflow designer with React Flow
- Real-time log streaming with WebSocket
- Network topology visualization
- Node configuration panels
- OAuth configuration wizard
- Advanced monitoring dashboards

## Contributing

See the main [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for guidelines.

---

**Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC™**  
**Licensed under the Apache License 2.0**
