/**
 * Formatter utilities for displaying data
 */

export const formatCurrency = (value, digits = 2) => {
  if (!value && value !== 0) return '-';
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    minimumFractionDigits: digits,
    maximumFractionDigits: digits,
  }).format(value);
};

export const formatPercent = (value, digits = 2) => {
  if (!value && value !== 0) return '-';
  return `${(value * 100).toFixed(digits)}%`;
};

export const formatPercentChange = (value, digits = 2) => {
  if (!value && value !== 0) return '-';
  const sign = value > 0 ? '+' : '';
  return `${sign}${(value * 100).toFixed(digits)}%`;
};

export const formatNumber = (value, digits = 2) => {
  if (!value && value !== 0) return '-';
  return parseFloat(value).toFixed(digits);
};

export const formatDate = (date, locale = 'en-US') => {
  if (!date) return '-';
  return new Intl.DateTimeFormat(locale).format(new Date(date));
};

export const formatDateTime = (date, locale = 'en-US') => {
  if (!date) return '-';
  return new Intl.DateTimeFormat(locale, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  }).format(new Date(date));
};

export const formatCompactNumber = (value) => {
  if (!value && value !== 0) return '-';
  const abs = Math.abs(value);
  if (abs >= 1e9) return `${(value / 1e9).toFixed(2)}B`;
  if (abs >= 1e6) return `${(value / 1e6).toFixed(2)}M`;
  if (abs >= 1e3) return `${(value / 1e3).toFixed(2)}K`;
  return value.toFixed(2);
};

export const formatSymbol = (symbol) => {
  if (!symbol) return '-';
  return symbol.toUpperCase();
};
