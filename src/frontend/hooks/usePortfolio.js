/**
 * usePortfolio - Portfolio state management hook
 * Manages portfolio data, loading states, and operations
 */

import { useState, useEffect } from 'react';
import { getPortfolioHistory } from '../services/api';

const usePortfolio = () => {
  const [portfolioData, setPortfolioData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadPortfolio = async () => {
      setLoading(true);
      try {
        const savedPortfolioId = localStorage.getItem('currentPortfolioId');
        if (savedPortfolioId) {
          const data = await getPortfolioHistory(savedPortfolioId);
          setPortfolioData(data);
        }
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadPortfolio();
  }, []);

  const optimize = async (config) => {
    setLoading(true);
    try {
      const result = await optimizePortfolio(config);
      setPortfolioData(result);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const save = async (data) => {
    try {
      const result = await savePortfolio(data);
      localStorage.setItem('currentPortfolioId', result.id);
      setPortfolioData(result);
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    }
  };

  return {
    portfolioData,
    loading,
    error,
    optimize,
    save,
  };
};

export default usePortfolio;
