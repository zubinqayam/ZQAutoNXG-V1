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
- Vercel Speed Insights integration for performance monitoring

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

This frontend includes Vercel Speed Insights integration for monitoring performance metrics. To enable Speed Insights:

1. **Vercel Account Setup**: Ensure you have a Vercel account and a project on Vercel
2. **Enable Speed Insights**: In the Vercel dashboard, select your project and enable the Speed Insights tab
3. **Deploy to Vercel**: Push your changes to deploy the application to Vercel using:
   ```bash
   vercel deploy
   ```
4. **View Metrics**: Once deployed and after users visit your site, view performance data in the Speed Insights dashboard tab

The Speed Insights tracking script (`/_vercel/speed-insights/script.js`) is automatically loaded and will collect performance metrics about your application's user experience, including:
- Core Web Vitals (LCP, FID, CLS)
- Page load performance
- User interaction metrics

**Note**: Speed Insights will only function when deployed to Vercel. Local development will not send data to the Speed Insights dashboard.

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
