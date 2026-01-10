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
- **Vercel Speed Insights integration** - Automatic Web Vitals monitoring when deployed to Vercel

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

## Vercel Speed Insights

The frontend includes Vercel Speed Insights tracking to monitor Web Vitals performance metrics when deployed to Vercel.

### Setup

Speed Insights is already integrated into the HTML frontend. To enable it:

1. **Enable on Vercel Dashboard**
   - Go to your [Vercel Dashboard](https://vercel.com/dashboard)
   - Select the ZQAutoNXG project
   - Click the **Speed Insights** tab
   - Click **Enable**

2. **Deploy to Vercel**
   ```bash
   vercel deploy
   ```

3. **View Metrics**
   - After deployment and user visits, metrics will appear in your Speed Insights dashboard
   - Access them from the **Speed Insights** tab in your project settings

For detailed setup and usage instructions, see [docs/SPEED_INSIGHTS.md](../docs/SPEED_INSIGHTS.md).

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
