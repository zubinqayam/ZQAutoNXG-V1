# ZQAutoNXG + Precedent Integration Guide

## Overview

This guide documents the successful integration of the **Precedent Next.js template** into the ZQAutoNXG automation platform. Precedent is a popular, production-ready Next.js starter kit created by Steven Tey, featuring modern React components, TypeScript, Tailwind CSS, and a collection of useful utilities.

## What is Precedent?

Precedent is an opinionated collection of components, hooks, and utilities for Next.js projects, providing:

- **Next.js 14** with App Router
- **TypeScript** for end-to-end type safety
- **Tailwind CSS** for rapid UI development
- **Radix UI** for accessible component primitives
- **Framer Motion** for smooth animations
- **Lucide Icons** for beautiful, consistent iconography
- **Custom Hooks** for common React patterns
- **Utility Functions** for formatting and manipulation

**Official Resources:**
- Website: https://precedent.dev
- Repository: https://github.com/steven-tey/precedent
- Vercel Template: https://vercel.com/templates/next.js/precedent

## Integration Components

### Directory Structure

The integration adds a new `web/` directory containing the Next.js application:

```
ZQAutoNXG-V1/
├── web/                           # Next.js Frontend (NEW)
│   ├── app/                      # Next.js App Router
│   │   ├── layout.tsx           # Root layout with Inter font
│   │   ├── page.tsx             # Home page with platform overview
│   │   ├── globals.css          # Global Tailwind styles
│   │   ├── workflows/           # Workflow management page
│   │   │   └── page.tsx
│   │   └── health/              # System health monitoring page
│   │       └── page.tsx
│   ├── components/              # React components
│   │   └── ui/                 # Reusable UI components
│   │       ├── card.tsx        # Card component with variants
│   │       └── badge.tsx       # Badge component with status colors
│   ├── lib/                    # Utilities and hooks
│   │   ├── utils.ts           # Utility functions (cn, nFormatter, etc.)
│   │   └── hooks/             # Custom React hooks
│   │       ├── use-intersection-observer.ts
│   │       ├── use-local-storage.ts
│   │       └── use-scroll.ts
│   ├── public/                # Static assets
│   │   └── robots.txt
│   ├── package.json           # Node.js dependencies
│   ├── next.config.js         # Next.js configuration with API proxy
│   ├── tsconfig.json          # TypeScript configuration
│   ├── tailwind.config.js     # Tailwind CSS theme
│   ├── postcss.config.js      # PostCSS configuration
│   ├── prettier.config.js     # Code formatting
│   ├── .eslintrc.json         # Linting rules
│   ├── .env.example           # Environment variables template
│   ├── .gitignore             # Git ignore for Node.js
│   ├── Dockerfile             # Container build configuration
│   └── README.md              # Frontend documentation
```

### Key Files Added

#### Configuration Files

1. **package.json** - Node.js dependencies including:
   - Next.js 14.0.4
   - React 18.2.0
   - Tailwind CSS 3.4.0
   - Radix UI components
   - Framer Motion
   - Lucide React icons
   - TypeScript and development tools

2. **next.config.js** - Next.js configuration with:
   - Standalone output for Docker
   - API proxy to backend (localhost:8000)
   - Optimizations enabled

3. **tailwind.config.js** - Custom theme with:
   - Primary color palette (purple/blue gradient)
   - Custom animations
   - Font configuration for Inter

4. **tsconfig.json** - TypeScript configuration with:
   - Path aliases (@/components, @/lib)
   - Strict type checking
   - Next.js plugin integration

#### Application Files

1. **app/layout.tsx** - Root layout featuring:
   - Inter font from next/font/google
   - Meta tags for SEO
   - Gradient background styling

2. **app/page.tsx** - Home page with:
   - Platform status display
   - Feature showcase cards
   - Quick action buttons
   - Responsive grid layout

3. **app/workflows/page.tsx** - Workflow management page with:
   - Workflow list/grid view
   - Create workflow button
   - Individual workflow cards with details

4. **app/health/page.tsx** - System health monitoring with:
   - Overall system status
   - Component status breakdown
   - Status icons (CheckCircle, XCircle, AlertCircle)
   - Raw JSON response viewer

#### UI Components

1. **components/ui/card.tsx** - Flexible card component:
   - Card container
   - CardHeader, CardTitle, CardDescription
   - CardContent, CardFooter
   - Responsive styling

2. **components/ui/badge.tsx** - Badge component with variants:
   - default, secondary, success, destructive, outline
   - Status indicators for workflows and health

#### Utilities

1. **lib/utils.ts** - Helper functions from Precedent:
   - `cn()` - Merge Tailwind classes with proper precedence
   - `nFormatter()` - Format numbers (1.2K, 1.2M, etc.)
   - `capitalize()` - Capitalize first letter of strings
   - `truncate()` - Truncate strings with ellipsis

2. **lib/hooks/use-intersection-observer.ts** - Observe element visibility:
   - Useful for lazy loading and scroll animations
   - Configurable threshold and root margin

3. **lib/hooks/use-local-storage.ts** - Persist state in localStorage:
   - React hook for localStorage with JSON serialization
   - Error handling for storage access

4. **lib/hooks/use-scroll.ts** - Track scroll position:
   - Returns boolean based on scroll threshold
   - Useful for sticky headers and scroll effects

## API Integration

### Backend Proxy Configuration

The Next.js application proxies API requests to the FastAPI backend using Next.js rewrites in `next.config.js`:

```javascript
async rewrites() {
  return [
    {
      source: '/api/:path*',
      destination: 'http://localhost:8000/api/:path*',
    },
    {
      source: '/health',
      destination: 'http://localhost:8000/health',
    },
    {
      source: '/metrics',
      destination: 'http://localhost:8000/metrics',
    },
  ];
}
```

This allows the frontend to make requests to `/api/v1/workflows` which are automatically forwarded to `http://localhost:8000/api/v1/workflows`.

### Server-Side Data Fetching

Pages use Next.js 14 server components with async data fetching:

```typescript
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
```

Benefits:
- No client-side JavaScript for initial load
- Better SEO
- Faster perceived performance
- Automatic error handling

## Setup Instructions

### Prerequisites

- **Node.js 18+** installed
- **npm, yarn, or pnpm** package manager
- **ZQAutoNXG backend** running on port 8000

### Installation

```bash
# Navigate to web directory
cd web

# Install dependencies
npm install
# or
yarn install
# or
pnpm install
```

### Development

```bash
# Start development server
npm run dev

# The application will be available at:
# http://localhost:3000
```

The development server includes:
- Hot module replacement
- Fast refresh
- API proxy to backend
- TypeScript type checking

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

### Docker Deployment

```bash
# Build Docker image
cd web
docker build -t zqautonxg-web:latest .

# Run container
docker run -d \
  --name zqautonxg-web \
  -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  zqautonxg-web:latest
```

The Dockerfile uses:
- Multi-stage build for smaller image size
- Non-root user (nextjs:nodejs)
- Health checks
- Standalone output for optimal container size

## Features Implemented

### 1. Home Page (/)

- **Platform Overview** - Displays ZQAutoNXG branding and version
- **Status Badge** - Real-time operational status
- **Feature Cards** - Showcase key capabilities
  - AI-Powered Automation
  - Global-Scale Orchestration
  - Enterprise Security
- **Quick Actions** - Links to documentation and API
- **Responsive Design** - Works on mobile, tablet, desktop

### 2. Workflows Page (/workflows)

- **Workflow List** - Grid view of all workflows
- **Create Button** - Initiate new workflow creation
- **Workflow Cards** - Display workflow details:
  - Name and ID
  - Status badge
  - Node and edge counts
  - View/Edit actions
- **Empty State** - Helpful message when no workflows exist

### 3. Health Page (/health)

- **Overall Status** - System-wide health indicator
- **Component Breakdown** - Individual component status
- **Status Icons** - Visual indicators (✓, ⚠, ✗)
- **Timestamp** - Last update time
- **Raw Response** - JSON viewer for debugging

### 4. UI Components

- **Card** - Flexible container component
- **Badge** - Status indicators with color variants
- **Animations** - Smooth transitions with Framer Motion
- **Icons** - Lucide React icon library

### 5. Utilities

- **Class Management** - Tailwind class merging with `cn()`
- **Number Formatting** - Display large numbers as 1.2K, 1.2M
- **Text Utilities** - Capitalize and truncate functions
- **React Hooks** - Intersection observer, localStorage, scroll tracking

## Design System

### Color Palette

Primary colors based on ZQAutoNXG brand:

```javascript
primary: {
  50: '#f5f7ff',
  100: '#ebf0ff',
  200: '#cdd9ff',
  300: '#a3b9ff',
  400: '#667eea',  // Main brand color
  500: '#5568d3',
  600: '#4854c2',
  700: '#3d46a8',
  800: '#323a8d',
  900: '#2a3174',
}
```

### Typography

- **Font Family**: Inter (loaded via next/font/google)
- **Weights**: Regular (400), Medium (500), Semibold (600), Bold (700)
- **Optimized**: Automatic subsetting and preloading

### Animations

Custom Tailwind animations:
- `fade-up` - Fade in with upward motion
- `fade-down` - Fade in with downward motion
- `slide-up-fade` - Slide and fade for dropdowns
- `slide-down-fade` - Slide and fade for popovers

## Environment Variables

Create `.env.local` in the web directory:

```bash
# Backend API URL (development)
NEXT_PUBLIC_API_URL=http://localhost:8000

# Backend API URL (production)
# NEXT_PUBLIC_API_URL=https://api.zqautonxg.com

# Optional: Clerk Authentication (future)
# NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
# CLERK_SECRET_KEY=
```

## Testing

### Manual Testing Checklist

- [ ] Homepage loads and displays platform information
- [ ] Status badge shows correct backend status
- [ ] Feature cards are responsive
- [ ] Navigation links work
- [ ] Workflows page fetches and displays workflows
- [ ] Health page shows system status
- [ ] API proxy correctly forwards requests
- [ ] Mobile responsive design works
- [ ] Animations are smooth
- [ ] Loading states handled gracefully
- [ ] Error states handled appropriately

### Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Android)

## Troubleshooting

### Common Issues

1. **"Cannot connect to backend"**
   - Ensure ZQAutoNXG backend is running on port 8000
   - Check NEXT_PUBLIC_API_URL environment variable
   - Verify no CORS issues

2. **"Module not found" errors**
   - Run `npm install` to install dependencies
   - Clear `.next` directory and rebuild
   - Check node_modules is not in .gitignore

3. **Port 3000 already in use**
   - Change port: `PORT=3001 npm run dev`
   - Or stop other process using port 3000

4. **Build fails with TypeScript errors**
   - Check tsconfig.json is correct
   - Verify all @types packages are installed
   - Run `npx tsc --noEmit` to check types

5. **Styles not applying**
   - Ensure Tailwind CSS is configured
   - Check postcss.config.js exists
   - Verify globals.css is imported in layout.tsx

## Future Enhancements

The following features are planned for future releases:

### Short Term
- [ ] Add dark mode toggle
- [ ] Implement workflow editor with drag-and-drop
- [ ] Add WebSocket support for real-time logs
- [ ] Create node management pages
- [ ] Add authentication with Clerk
- [ ] Implement search functionality

### Medium Term
- [ ] Network topology visualization with React Flow
- [ ] Advanced monitoring dashboards
- [ ] User settings and preferences
- [ ] Workflow templates library
- [ ] Export/import workflows
- [ ] Multi-language support (i18n)

### Long Term
- [ ] Mobile app (React Native)
- [ ] Desktop app (Electron)
- [ ] Advanced analytics
- [ ] Collaborative editing
- [ ] Plugin system
- [ ] Custom theme builder

## Performance Optimization

### Current Optimizations

1. **Next.js 14 App Router** - Server components by default
2. **Standalone Output** - Minimal Docker image size
3. **Font Optimization** - next/font with preloading
4. **Image Optimization** - Automatic image optimization (when images added)
5. **Code Splitting** - Automatic page-based code splitting

### Recommended Optimizations

1. **Static Generation** - Use `generateStaticParams` for static pages
2. **Incremental Static Regeneration** - For frequently updated pages
3. **React Server Components** - Keep using for data fetching
4. **Client Components** - Only when interactivity needed
5. **Bundle Analysis** - Use `@next/bundle-analyzer`

## Security Considerations

### Implemented

1. **Non-root Docker User** - Container runs as nextjs:nodejs
2. **Environment Variables** - Sensitive data in .env files
3. **API Proxy** - Hides backend URL from client
4. **TypeScript** - Type safety reduces bugs
5. **ESLint** - Code quality and security rules

### Recommended

1. **Content Security Policy** - Add CSP headers
2. **Rate Limiting** - Implement on API routes
3. **Input Validation** - Validate all user inputs
4. **XSS Protection** - Sanitize any user-generated content
5. **HTTPS Only** - Use SSL in production

## Contributing

### Code Style

- **TypeScript**: All new code should use TypeScript
- **Formatting**: Run `npm run format` before committing
- **Linting**: Run `npm run lint` to check for issues
- **Components**: Use functional components with hooks
- **Naming**: PascalCase for components, camelCase for functions

### Pull Request Process

1. Create a feature branch from `main`
2. Implement changes with proper TypeScript types
3. Add/update tests as needed
4. Run linting and formatting
5. Update documentation
6. Submit PR with clear description

## Resources

### Documentation

- **Next.js**: https://nextjs.org/docs
- **React**: https://react.dev
- **Tailwind CSS**: https://tailwindcss.com/docs
- **TypeScript**: https://www.typescriptlang.org/docs
- **Precedent**: https://precedent.dev

### Community

- **GitHub Repository**: https://github.com/zubinqayam/ZQAutoNXG-V1
- **Issues**: https://github.com/zubinqayam/ZQAutoNXG-V1/issues
- **Contact**: zubin.qayam@outlook.com

## License

Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC™

Licensed under the Apache License, Version 2.0. See LICENSE file for details.

### Acknowledgments

- **Precedent** by Steven Tey - https://precedent.dev
- **Next.js** by Vercel - https://nextjs.org
- **Tailwind CSS** by Tailwind Labs - https://tailwindcss.com
- **Radix UI** - https://www.radix-ui.com
- **Lucide Icons** - https://lucide.dev

---

**Last Updated**: 2026-01-10  
**Version**: 6.0.0  
**Author**: Zubin Qayam
