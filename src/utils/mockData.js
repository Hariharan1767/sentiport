/**
 * Mock data for development and testing
 */

export const mockPortfolios = [
  {
    id: '1',
    name: 'Tech Growth',
    stocks: ['AAPL', 'GOOGL', 'MSFT'],
    weights: [0.35, 0.35, 0.3],
    sentimentWeights: [0.4, 0.35, 0.25],
    createdAt: '2024-01-15',
    metrics: {
      annualReturn: 0.245,
      sharpeRatio: 1.85,
      volatility: 0.123,
      maxDrawdown: -0.085,
    },
  },
];

export const mockStocks = [
  { symbol: 'AAPL', name: 'Apple Inc.', price: 150.25, change: 2.5 },
  { symbol: 'GOOGL', name: 'Alphabet Inc.', price: 140.15, change: 1.8 },
  { symbol: 'MSFT', name: 'Microsoft Corp.', price: 380.45, change: 3.2 },
  { symbol: 'AMZN', name: 'Amazon.com Inc.', price: 175.30, change: 2.1 },
  { symbol: 'TSLA', name: 'Tesla Inc.', price: 245.80, change: -1.5 },
  { symbol: 'META', name: 'Meta Platforms Inc.', price: 380.50, change: 4.2 },
  { symbol: 'NVDA', name: 'NVIDIA Corp.', price: 520.30, change: 5.1 },
  { symbol: 'JPM', name: 'JPMorgan Chase', price: 195.80, change: 1.2 },
  { symbol: 'BAC', name: 'Bank of America', price: 35.40, change: 0.8 },
  { symbol: 'WMT', name: 'Walmart Inc.', price: 85.50, change: 0.5 },
];

export const mockSentimentData = {
  AAPL: {
    score: 0.72,
    sentiment: 'Bullish',
    newsCount: 245,
    accuracy: 0.785,
  },
  GOOGL: {
    score: 0.68,
    sentiment: 'Bullish',
    newsCount: 198,
    accuracy: 0.762,
  },
  MSFT: {
    score: 0.75,
    sentiment: 'Bullish',
    newsCount: 267,
    accuracy: 0.798,
  },
  AMZN: {
    score: 0.65,
    sentiment: 'Neutral',
    newsCount: 156,
    accuracy: 0.721,
  },
  TSLA: {
    score: 0.45,
    sentiment: 'Neutral',
    newsCount: 389,
    accuracy: 0.695,
  },
};

export const mockPerformanceData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
  datasets: [
    {
      label: 'Sentiment Portfolio',
      data: [100, 105, 103, 108, 112, 115, 118, 122, 125, 128, 132, 138],
      borderColor: '#00FF88',
      backgroundColor: 'rgba(0, 255, 136, 0.1)',
      tension: 0.4,
    },
    {
      label: 'Traditional Portfolio',
      data: [100, 102, 101, 104, 107, 109, 111, 113, 115, 117, 119, 122],
      borderColor: '#FFB800',
      backgroundColor: 'rgba(255, 184, 0, 0.1)',
      tension: 0.4,
    },
    {
      label: 'Benchmark',
      data: [100, 101, 100, 103, 105, 107, 108, 109, 110, 111, 112, 113],
      borderColor: '#1A1F3A',
      backgroundColor: 'rgba(26, 31, 58, 0.1)',
      tension: 0.4,
    },
  ],
};

export const mockAllocationData = {
  labels: ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'],
  datasets: [
    {
      data: [25, 20, 20, 20, 15],
      backgroundColor: ['#00FF88', '#FFB800', '#00D4FF', '#FF6B9D', '#FFD700'],
      borderColor: '#0A0E27',
      borderWidth: 2,
    },
  ],
};
