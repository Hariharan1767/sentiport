## SentiPort Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (React)                         │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              Pages & Views                           │   │
│  │  - Dashboard      - Optimizer                        │   │
│  │  - Analysis       - Settings                         │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Custom Hooks & State Management              │   │
│  │  - usePortfolio   - useStocks   - useSentiment       │   │
│  │  - useForm        - useToast    - useChart           │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │            API Service Layer (Axios)                 │   │
│  │  - Portfolio Operations    - Stock Data              │   │
│  │  - Sentiment Analysis      - Backtesting             │   │
│  │  - Settings Management                               │   │
│  └──────────────────────────────────────────────────────┘   │
│                          ▼                                    │
├─────────────────────────────────────────────────────────────┤
│                  HTTP Communication                          │
├─────────────────────────────────────────────────────────────┤
│                          ▼                                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │             Backend API Server                       │   │
│  │  (Not included - connect your own)                   │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Component Hierarchy

```
App
├── Navigation
│   ├── Logo
│   └── NavLinks (Mobile & Desktop)
└── Main Content
    ├── Dashboard
    │   ├── StatCard x4
    │   ├── Card (Portfolio Allocation)
    │   └── Card (Sentiment Analysis)
    ├── Optimize
    │   ├── Card (Stock Selection)
    │   ├── Card (Parameters)
    │   └── Button (Optimize)
    ├── Analysis
    │   ├── Tab Navigation
    │   ├── PerformanceChart
    │   ├── Card (Model Performance)
    │   └── Card (Data Quality)
    └── Settings
        ├── Card (Data Source)
        ├── Card (Model Settings)
        ├── Card (Portfolio Settings)
        └── Buttons (Save/Reset)
```

### Data Flow

```
User Action
    ▼
Component Event Handler
    ▼
Hook (useForm, useToast, etc.)
    ▼
API Service (api.js)
    ▼
Axios Interceptors
    ▼
Backend API
    ▼
Response
    ▼
State Update
    ▼
Component Re-render
```

### State Management Pattern

Each feature uses a dedicated hook:

```
usePortfolio
├── State: portfolioData, loading, error
├── Methods: optimize(), save(), load()
└── Auto-fetch on mount

useStocks
├── State: stocks, selectedStocks, loading
├── Methods: search(), select(), deselect()
└── Debounced search, localStorage persistence

useSentiment
├── State: sentimentData, loading, error
├── Methods: fetch(), fetchBulk(), refresh()
└── Caching strategy

useForm
├── State: values, errors, touched, isSubmitting
├── Methods: handleChange(), handleSubmit(), resetForm()
└── Generic form handler with validation
```

### API Integration

The API service layer (`src/services/api.js`) provides:

1. **Request Interceptors**
   - Add authentication tokens
   - Request logging

2. **Response Interceptors**
   - Extract data from responses
   - Automatic retry on network errors (3 attempts)
   - Error mapping

3. **Endpoints**
   - Portfolio Operations
   - Stock Data
   - Sentiment Analysis
   - Backtesting
   - User Settings

### Design System

**Colors**
- Primary: #0A0E27 (Dark Blue)
- Secondary: #1A1F3A
- Accent: #00FF88 (Electric Green)
- Warning: #FFB800
- Danger: #FF3860

**Typography**
- UI Font: Epilogue (weights: 300-800)
- Data Font: Space Mono (monospace)

**Effects**
- Glassmorphism (backdrop blur)
- Glow effects (box-shadow)
- Smooth transitions (0.3s)
- Animated gradients

### Responsive Breakpoints

- **Mobile**: 320px - 767px
- **Tablet**: 768px - 1023px
- **Desktop**: 1024px - 1439px
- **Large Desktop**: 1440px+

### Performance Optimizations

1. **Code Splitting**
   - Route-based lazy loading
   - Component-level code splitting

2. **Memoization**
   - useMemo for expensive calculations
   - useCallback for event handlers
   - React.memo for component memoization

3. **Caching**
   - useRef for sentiment cache
   - localStorage for preferences
   - API response caching

4. **Debouncing**
   - Search input debouncing (300ms)
   - Form input validation debouncing

### Testing Strategy

```
Unit Tests
├── API service
├── Hooks
└── Utility functions

Integration Tests
├── Form workflows
├── Data fetching
└── Component interactions

E2E Tests
├── Full user flows
├── Mobile viewports
└── Accessibility
```

### Deployment Ready

**Build Process**
```bash
npm run build
# Outputs to dist/ directory
# Minified, optimized assets
```

**Environment Configuration**
```
.env (development)
.env.production (production)
VITE_API_URL=your_api_endpoint
```

**Hosting Options**
- Vercel
- Netlify
- GitHub Pages
- Custom servers

---

This architecture provides a solid foundation for a modern, scalable portfolio optimization application.
