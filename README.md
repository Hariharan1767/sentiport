# SentiPort - Sentiment-Driven Portfolio Optimization

A modern, production-ready React web application for sentiment-driven portfolio optimization using Vite, Tailwind CSS, and Chart.js.

## Features

- **Sentiment Analysis**: Leverage NLP models to analyze market sentiment
- **Portfolio Optimization**: Use Mean-Variance optimization with sentiment weighting
- **Interactive Dashboard**: Real-time portfolio metrics and visualization
- **Responsive Design**: Mobile-first approach with dark mode aesthetic
- **Performance Analytics**: Comprehensive backtesting and performance metrics
- **Customizable Settings**: Configure data sources, models, and portfolio parameters

## Tech Stack

- **Frontend Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS + Custom CSS
- **Visualization**: Chart.js + React-Chartjs-2
- **HTTP Client**: Axios
- **Animation**: Framer Motion
- **Icons**: Lucide React
- **Code Quality**: ESLint + Prettier

## Project Structure

```
src/
├── components/
│   ├── common/          # Reusable components (Card, Button, Input, etc.)
│   ├── charts/          # Chart components
│   ├── Navigation.jsx
│   ├── Dashboard.jsx
│   ├── Optimize.jsx
│   ├── Analysis.jsx
│   └── Settings.jsx
├── services/
│   └── api.js          # Centralized API client
├── hooks/              # Custom React hooks
├── utils/              # Helper functions & utilities
├── styles/
│   └── globals.css     # Global styles with design system
└── App.jsx
```

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd SentiPort
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API configuration
   ```

## Available Scripts

### Development
```bash
npm run dev
```
Starts the development server at `http://localhost:5173`

### Build
```bash
npm run build
```
Creates an optimized production build

### Preview
```bash
npm run preview
```
Previews the production build locally

### Linting
```bash
npm run lint
npm run lint:fix
```
Run ESLint to check code quality

### Formatting
```bash
npm run format
```
Format code with Prettier

## Environment Variables

```env
VITE_API_URL=http://localhost:3000/api
VITE_APP_NAME=SentiPort
VITE_APP_VERSION=1.0.0
```

## Design System

### Colors
- **Primary**: #0A0E27 (Dark Blue)
- **Secondary**: #1A1F3A
- **Accent**: #00FF88 (Electric Green)
- **Warning**: #FFB800
- **Danger**: #FF3860

### Typography
- **UI Font**: Epilogue (300, 400, 600, 700, 800)
- **Data Font**: Space Mono (400, 700)

### Features
- Glassmorphism effects
- Animated gradients
- Custom glow effects
- Responsive breakpoints (320px, 768px, 1024px, 1440px)
- Dark mode support

## Quick Start Guide

### 1. Create a Portfolio
Navigate to the **Optimize** page and:
- Select 3+ stocks
- Configure sentiment weight (λ)
- Set risk-free rate
- Choose date range

### 2. View Analytics
Check the **Dashboard** for:
- Key performance metrics
- Portfolio allocation
- Sentiment analysis

### 3. Deep Dive Analysis
Use the **Analysis** tab to:
- Compare portfolio strategies
- Review performance charts
- Analyze sentiment impact

### 4. Customize Settings
Go to **Settings** to:
- Connect data sources
- Configure sentiment model
- Set portfolio constraints

## API Integration

The app uses a centralized API client in `src/services/api.js`:

```javascript
import { optimizePortfolio, getBulkSentiment } from './services/api';

// Example usage
const result = await optimizePortfolio({
  stocks: ['AAPL', 'GOOGL'],
  lambda: 0.5,
  riskFreeRate: 0.05,
  startDate: '2023-01-01',
  endDate: '2024-01-01'
});
```

## Performance Optimization

- Code splitting by route
- Lazy loading for heavy components
- Memoization (useMemo, useCallback)
- Request caching
- Responsive image optimization

## Accessibility

- ARIA labels and semantic HTML
- Focus management
- Keyboard navigation support
- High contrast dark theme
- Reduced motion support

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Development Workflow

1. Create feature branches
2. Follow ESLint rules
3. Format with Prettier
4. Test thoroughly
5. Submit pull requests

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Follow the code style
4. Submit a pull request

## License

MIT License - see LICENSE file for details

## Support

For issues and feature requests, please use the GitHub issue tracker.

---

Built with passion for better portfolio management through sentiment analysis.
