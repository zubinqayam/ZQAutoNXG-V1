# Vercel Web Analytics Setup Guide for ZQAutoNXG

This guide explains how to set up and use Vercel Web Analytics with the ZQAutoNXG platform.

## Overview

Vercel Web Analytics is a privacy-preserving analytics solution that helps you understand user interactions with your application. It requires:

1. A Vercel account and project
2. Web Analytics enabled in the Vercel dashboard
3. Analytics tracking code in your frontend
4. Deployment to Vercel

## Prerequisites

- A [Vercel account](https://vercel.com/signup) (free or paid)
- A Vercel project connected to your repository
- Node.js 18+ for managing frontend dependencies

## Setup Steps

### Step 1: Enable Web Analytics in Vercel Dashboard

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your ZQAutoNXG project
3. Click the **Analytics** tab
4. Click **Enable** in the dialog

> **Note:** Enabling Web Analytics will add new routes (scoped at `/_vercel/insights/*`) after your next deployment.

### Step 2: Install Frontend Dependencies

The analytics package is already configured in `frontend/package.json`. Install it:

```bash
# Using npm
npm install

# Using pnpm
pnpm install

# Using yarn
yarn install

# Using bun
bun install
```

This installs `@vercel/analytics` which provides tracking functionality.

### Step 3: Verify Analytics Integration

The analytics are already integrated in the frontend:

- **Script Tag**: `frontend/index.html` includes the Vercel insights script
- **Event Tracking**: Custom events are tracked for:
  - Page views
  - Workflow creation
  - Workflow viewing

### Step 4: Deploy to Vercel

Deploy your application using the Vercel CLI:

```bash
# Install Vercel CLI if not already installed
npm install -g vercel

# Deploy from the repository root
vercel deploy
```

Or, if you've connected your Git repository, simply push to your main branch:

```bash
git push origin main
```

Vercel will automatically deploy your changes.

### Step 5: View Analytics Data

Once deployed and users visit your site:

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your ZQAutoNXG project
3. Click the **Analytics** tab
4. Explore your data by viewing and filtering the panels

> **Note:** Initial data collection may take a few minutes. After a few days of visitor activity, you'll have enough data to start exploring meaningful insights.

## Custom Events

The following custom events are already tracked in the application:

### Page View
```javascript
window.va('event', {
    name: 'page_view',
    data: {
        page: document.location.pathname,
        referrer: document.referrer,
    }
});
```

### Workflow Created
```javascript
window.va('event', {
    name: 'workflow_created',
    data: { workflow_id: data.id }
});
```

### Workflows Viewed
```javascript
window.va('event', {
    name: 'workflows_viewed',
    data: { workflow_count: workflows.length }
});
```

### Adding More Custom Events

To add additional custom events to your application:

```javascript
if (typeof window !== 'undefined' && window.va) {
    window.va('event', {
        name: 'your_event_name',
        data: { 
            // Add relevant data here
            key: 'value'
        }
    });
}
```

Update the events in `frontend/index.html` as needed.

## Configuration for Different Deployment Targets

### For Local Development

Web Analytics tracking is only active when deployed to Vercel. Local development will not send analytics data (the scripts will fail silently, which is expected behavior).

### For Production Deployment

When deployed to Vercel, the analytics will automatically work. The `/_vercel/insights/script.js` endpoint is provided by Vercel's infrastructure.

## Architecture Notes

### Backend (FastAPI)
- The FastAPI backend serves the frontend and supports static file serving
- A mount point for `/_vercel/insights` is configured for Vercel's analytics infrastructure
- No backend changes are required for analytics functionality

### Frontend (HTML/JavaScript)
- Simple HTML interface with vanilla JavaScript
- Analytics tracking is non-blocking and deferred
- Events are automatically sent to Vercel when the page loads

## Troubleshooting

### Analytics Not Showing Data

1. **Verify Deployment**: Ensure your app is deployed to Vercel
2. **Check Script Tag**: Verify `/_vercel/insights/script.js` is loading in browser dev tools Network tab
3. **Wait for Data**: Initial data may take several minutes to appear
4. **Check Events**: Use browser dev tools Console to verify `window.va` is defined

### Missing Custom Events

1. **Verify Event Code**: Check that event tracking code is present in `index.html`
2. **Check Browser Console**: Look for any JavaScript errors
3. **Verify va() Function**: Ensure `window.va` is properly defined before calling it

### Events Not Appearing in Dashboard

1. Ensure at least one visitor has accessed the page
2. Wait a few minutes for data to propagate
3. Check that events use simple, descriptive names
4. Verify you're looking at the correct Vercel project

## Privacy and Compliance

Vercel Web Analytics is designed with privacy in mind:

- No cookies are set by default
- No user data is stored in a database
- GDPR-compliant data handling
- No sensitive data collection

For more information, see [Vercel Analytics Privacy Policy](/docs/analytics/privacy-policy)

## Next Steps

1. **Monitor Performance**: Use the Analytics dashboard to understand user behavior
2. **Add Custom Events**: Track important business metrics specific to your use case
3. **Filter Data**: Use filtering to analyze subsets of your traffic
4. **Set Alerts**: Configure alerts for anomalies in your analytics (on Pro/Enterprise plans)

## References

- [Vercel Web Analytics Documentation](https://vercel.com/docs/analytics)
- [@vercel/analytics Package](https://www.npmjs.com/package/@vercel/analytics)
- [Vercel Deployment Documentation](https://vercel.com/docs/concepts/git)

## Support

For issues with Vercel Web Analytics:
- Check [Vercel Troubleshooting Guide](/docs/analytics/troubleshooting)
- Visit [Vercel Community Forums](https://github.com/vercel/feedback)
- Contact [Vercel Support](https://vercel.com/support)

---

**ZQAutoNXG v6.0.0** - Architecture: G V2 NovaBase  
Copyright © 2025 Zubin Qayam — Apache 2.0 License
