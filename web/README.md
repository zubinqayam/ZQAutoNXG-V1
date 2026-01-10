# ZQAutoNXG Web Frontend

**Next.js 14 Application powered by Precedent**

This is the modern web frontend for ZQAutoNXG, built with Next.js 14 and styled using the Precedent template architecture.

## 🚀 Features

- **Next.js 14** - Latest React framework with App Router
- **TypeScript** - End-to-end type safety
- **Tailwind CSS** - Utility-first CSS framework
- **Radix UI** - Accessible UI primitives
- **Framer Motion** - Smooth animations
- **Lucide Icons** - Beautiful icon library
- **Precedent Utilities** - Collection of useful hooks and helpers

## 📋 Prerequisites

- Node.js 18.0.0 or higher
- npm, yarn, or pnpm
- ZQAutoNXG backend running on `http://localhost:8000`

## 🛠️ Installation

```bash
# Navigate to web directory
cd web

# Install dependencies with your preferred package manager
npm install
# or
yarn install
# or
pnpm install
```

## 🏃 Running Development Server

```bash
# Start the development server
npm run dev
# or
yarn dev
# or
pnpm dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

The development server includes:
- Hot reload
- Fast refresh
- API proxy to backend (configured in `next.config.js`)

## 🏗️ Building for Production

```bash
# Build the application
npm run build

# Start production server
npm run start
```

## 📁 Project Structure

```
web/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout with fonts
│   ├── page.tsx           # Home page
│   └── globals.css        # Global styles
├── components/            # React components
│   └── ui/               # Reusable UI components
│       ├── card.tsx      # Card component
│       └── badge.tsx     # Badge component
├── lib/                   # Utilities and hooks
│   ├── utils.ts          # Utility functions
│   └── hooks/            # Custom React hooks
│       ├── use-intersection-observer.ts
│       ├── use-local-storage.ts
│       └── use-scroll.ts
├── public/               # Static assets
├── .env.example          # Environment variables template
├── next.config.js        # Next.js configuration
├── tailwind.config.js    # Tailwind CSS configuration
├── tsconfig.json         # TypeScript configuration
└── package.json          # Dependencies and scripts
```

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file in the web directory:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### API Integration

The frontend is configured to proxy API requests to the backend:

- `/api/*` → `http://localhost:8000/api/*`
- `/health` → `http://localhost:8000/health`
- `/metrics` → `http://localhost:8000/metrics`

Configuration is in `next.config.js`.

## 🎨 Styling

This project uses Tailwind CSS with a custom theme:

- Primary colors based on ZQAutoNXG brand (purple/blue gradient)
- Custom animations for smooth UI transitions
- Responsive design utilities
- Dark mode support (optional)

### Custom Utilities

The project includes several utility functions from Precedent:

- `cn()` - Merge Tailwind classes with proper precedence
- `nFormatter()` - Format numbers (1.2K, 1.2M)
- `capitalize()` - Capitalize first letter
- `truncate()` - Truncate strings with ellipsis

### Custom Hooks

- `useIntersectionObserver` - Observe element visibility
- `useLocalStorage` - Persist state in localStorage
- `useScroll` - Track scroll position

## 📚 Component Library

### UI Components

- **Card** - Container component with variants
- **Badge** - Label component with multiple styles

More components will be added as needed.

## 🔗 API Integration

The frontend communicates with the ZQAutoNXG backend API:

```typescript
// Example API call
const response = await fetch('/api/v1/workflows');
const workflows = await response.json();
```

Server-side rendering is used where appropriate for optimal performance.

## 🧪 Development

### Code Quality

```bash
# Lint code
npm run lint

# Format code
npm run format
```

### Best Practices

- Use TypeScript for type safety
- Follow React best practices
- Use server components where possible (Next.js 14 App Router)
- Implement proper error handling
- Use semantic HTML
- Ensure accessibility

## 🚀 Deployment

### Vercel (Recommended)

The easiest way to deploy is using [Vercel](https://vercel.com):

1. Push code to GitHub
2. Import project in Vercel
3. Configure environment variables
4. Deploy

### Docker

Build and run with Docker:

```bash
# Build Docker image
docker build -t zqautonxg-web .

# Run container
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:8000 \
  zqautonxg-web
```

### Static Export

For static hosting:

```bash
# Add to next.config.js
output: 'export'

# Build
npm run build

# Deploy the 'out' directory
```

## 🎯 Roadmap

Future enhancements planned:

- [ ] Drag-and-drop workflow designer
- [ ] Real-time WebSocket log streaming
- [ ] Network topology visualization
- [ ] Advanced monitoring dashboards
- [ ] User authentication with Clerk
- [ ] Dark mode toggle
- [ ] Additional page routes (workflows, nodes, etc.)

## 🤝 Contributing

When contributing to the frontend:

1. Follow the existing code style
2. Use TypeScript for all new code
3. Add proper type definitions
4. Test components thoroughly
5. Ensure accessibility standards
6. Update documentation

## 📄 License

Copyright © 2025 Zubin Qayam — ZQAutoNXG Powered by ZQ AI LOGIC™  
Licensed under the Apache License 2.0

## 🙏 Acknowledgments

- Built with [Precedent](https://precedent.dev) by Steven Tey
- Powered by [Next.js](https://nextjs.org)
- Styled with [Tailwind CSS](https://tailwindcss.com)
- Icons from [Lucide](https://lucide.dev)

---

**Questions?** Contact: zubin.qayam@outlook.com
