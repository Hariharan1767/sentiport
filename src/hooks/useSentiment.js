/**
 * useSentiment - Sentiment data fetching and caching hook
 */

import { useState, useCallback, useRef } from 'react';
import { analyzeSentiment, getBulkSentiment } from '../services/api';

const useSentiment = () => {
  const [sentimentData, setSentimentData] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const cacheRef = useRef({});

  const fetch = useCallback(async (symbol) => {
    if (cacheRef.current[symbol]) {
      setSentimentData((prev) => ({ ...prev, [symbol]: cacheRef.current[symbol] }));
      return cacheRef.current[symbol];
    }

    setLoading(true);
    try {
      const data = await analyzeSentiment(symbol);
      cacheRef.current[symbol] = data;
      setSentimentData((prev) => ({ ...prev, [symbol]: data }));
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const fetchBulk = useCallback(async (symbols) => {
    const uncached = symbols.filter((s) => !cacheRef.current[s]);
    if (uncached.length === 0) {
      const cached = symbols.reduce((acc, s) => {
        acc[s] = cacheRef.current[s];
        return acc;
      }, {});
      setSentimentData((prev) => ({ ...prev, ...cached }));
      return cached;
    }

    setLoading(true);
    try {
      const data = await getBulkSentiment(uncached);
      uncached.forEach((symbol, index) => {
        cacheRef.current[symbol] = data[index];
      });
      setSentimentData((prev) => ({ ...prev, ...data }));
      return data;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  const refresh = useCallback(async (symbol) => {
    delete cacheRef.current[symbol];
    return fetch(symbol);
  }, [fetch]);

  return {
    sentimentData,
    loading,
    error,
    fetch,
    fetchBulk,
    refresh,
  };
};

export default useSentiment;
