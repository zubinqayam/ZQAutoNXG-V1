# Vercel Speed Insights Setup

This guide explains how Vercel Speed Insights is integrated into the ZQAutoNXG project.

## Overview

ZQAutoNXG now includes Vercel Speed Insights to monitor and track Web Vitals performance metrics for the frontend interface. Speed Insights helps you understand how your application performs in production and identify optimization opportunities.

## Current Implementation

### Frontend Integration

The Vercel Speed Insights tracking script has been added to `frontend/index.html`. The integration follows the HTML implementation approach as documented in the [Vercel Speed Insights documentation](https://vercel.com/docs/speed-insights).

#### How It Works

1. **Initialization Script**: A global `window.si` function is defined to queue any data before the Speed Insights library loads
2. **Deferred Loading**: The Speed Insights script is loaded asynchronously after the page content loads
3. **Automatic Tracking**: Once loaded, Speed Insights automatically collects Web Vitals data (LCP, FID, CLS, etc.)

```html
<!-- Initialize the window.si function -->
<script>
    window.si = window.si || function () { (window.siq = window.siq || []).push(arguments); };
</script>

<!-- Load Speed Insights tracking script -->
<script defer src="/_vercel/speed-insights/script.js"></script>
```

## Prerequisite: Enable Speed Insights on Vercel

Before deploying to Vercel, you need to enable Speed Insights:

1. Go to the [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your ZQAutoNXG project
3. Click the **Speed Insights** tab
4. Click **Enable** to activate Speed Insights

**Note:** Enabling Speed Insights will create new routes scoped at `/_vercel/speed-insights/*` after your next deployment.

## Deployment

When you deploy ZQAutoNXG to Vercel:

1. The Speed Insights tracking script will be automatically served at `/_vercel/speed-insights/script.js` after you enable it
2. The frontend will automatically collect performance metrics from all visitors
3. Metrics will be available in your Vercel dashboard under the Speed Insights tab

### Deploy to Vercel

```bash
# Using Vercel CLI
vercel deploy

# Or push to your connected git repository
git push origin main
```

## Viewing Your Data

After deployment, metrics will start appearing in your dashboard:

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your ZQAutoNXG project
3. Click the **Speed Insights** tab

**Note:** It may take a few hours for initial data to appear as your users interact with the application.

## Monitoring Metrics

Speed Insights tracks the following Web Vitals:

- **LCP (Largest Contentful Paint)**: How quickly the page's main content loads
- **FID (First Input Delay)**: How responsive the page is to user interactions
- **CLS (Cumulative Layout Shift)**: How much layout shift happens during page load
- **TTFB (Time to First Byte)**: Time before first server response
- **FCP (First Contentful Paint)**: When the first content appears

## Future Enhancements

For future development with a React/Next.js frontend, consider using the `@vercel/speed-insights` npm package:

```bash
npm install @vercel/speed-insights
```

And integrate it as shown in the [official documentation](https://vercel.com/docs/speed-insights/getting-started).

## References

- [Vercel Speed Insights Documentation](https://vercel.com/docs/speed-insights)
- [Web Vitals Metrics](https://vercel.com/docs/speed-insights/metrics)
- [Privacy and Compliance](https://vercel.com/docs/speed-insights/privacy-policy)
- [Troubleshooting Guide](https://vercel.com/docs/speed-insights/troubleshooting)

## Support

For issues or questions about Speed Insights integration, please refer to:
- [Vercel Support Documentation](https://vercel.com/docs)
- [ZQAutoNXG Contributing Guidelines](./CONTRIBUTING.md)
