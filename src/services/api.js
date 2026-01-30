/**
 * Centralized API client using axios
 * Handles all backend communication with interceptors and retry logic
 */

import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

// Request interceptor
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor with retry logic
let retryCount = 0;
const MAX_RETRIES = 3;

apiClient.interceptors.response.use(
  (response) => {
    retryCount = 0;
    return response.data;
  },
  async (error) => {
    if (retryCount < MAX_RETRIES && (error.code === 'ECONNABORTED' || error.code === 'ERR_NETWORK')) {
      retryCount += 1;
      await new Promise((resolve) => setTimeout(resolve, 1000 * retryCount));
      return apiClient(error.config);
    }
    return Promise.reject(error);
  },
);

/**
 * Portfolio Operations
 */
export const optimizePortfolio = (stocks, lambda, riskFreeRate, startDate, endDate) =>
  apiClient.post('/portfolio/optimize', {
    stocks,
    lambda,
    riskFreeRate,
    startDate,
    endDate,
  });

export const getPortfolioHistory = (portfolioId) =>
  apiClient.get(`/portfolio/${portfolioId}/history`);

export const savePortfolio = (portfolioData) =>
  apiClient.post('/portfolio', portfolioData);

/**
 * Stock Data
 */
export const searchStocks = (query) =>
  apiClient.get('/stocks/search', { params: { q: query } });

export const getStockPrices = (symbol, startDate, endDate) =>
  apiClient.get(`/stocks/${symbol}/prices`, {
    params: { startDate, endDate },
  });

export const getStockInfo = (symbol) =>
  apiClient.get(`/stocks/${symbol}`);

/**
 * Sentiment Analysis
 */
export const analyzeSentiment = (symbol) =>
  apiClient.get(`/sentiment/${symbol}`);

export const getBulkSentiment = (symbols) =>
  apiClient.post('/sentiment/bulk', { symbols });

export const getSentimentHistory = (symbol, startDate, endDate) =>
  apiClient.get(`/sentiment/${symbol}/history`, {
    params: { startDate, endDate },
  });

/**
 * Backtesting
 */
export const runBacktest = (portfolioConfig) =>
  apiClient.post('/backtest', portfolioConfig);

export const getBacktestResults = (backtestId) =>
  apiClient.get(`/backtest/${backtestId}`);

/**
 * Settings
 */
export const saveUserSettings = (settings) =>
  apiClient.post('/settings', settings);

export const getUserSettings = () =>
  apiClient.get('/settings');

export default apiClient;
