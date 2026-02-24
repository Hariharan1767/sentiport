/**
 * useStocks - Stock data fetching and management hook
 */

import { useState, useCallback } from 'react';
import { searchStocks } from '../services/api';
import { debounce } from '../utils/helpers';

const useStocks = () => {
  const [stocks, setStocks] = useState([]);
  const [selectedStocks, setSelectedStocks] = useState([]);
  const [loading, setLoading] = useState(false);

  const debouncedSearch = useCallback(
    debounce(async (query) => {
      if (!query) {
        setStocks([]);
        return;
      }
      setLoading(true);
      try {
        const results = await searchStocks(query);
        setStocks(results);
      } catch (error) {
        console.error('Search failed:', error);
      } finally {
        setLoading(false);
      }
    }, 300),
    [],
  );

  const search = useCallback((query) => {
    debouncedSearch(query);
  }, [debouncedSearch]);

  const toggleStock = useCallback((stock) => {
    setSelectedStocks((prev) => {
      const updated = prev.includes(stock)
        ? prev.filter((s) => s !== stock)
        : [...prev, stock];
      localStorage.setItem('selectedStocks', JSON.stringify(updated));
      return updated;
    });
  }, []);

  const select = useCallback((stock) => {
    setSelectedStocks((prev) => {
      if (prev.includes(stock)) return prev;
      const updated = [...prev, stock];
      localStorage.setItem('selectedStocks', JSON.stringify(updated));
      return updated;
    });
  }, []);

  const deselect = useCallback((stock) => {
    setSelectedStocks((prev) => {
      const updated = prev.filter((s) => s !== stock);
      localStorage.setItem('selectedStocks', JSON.stringify(updated));
      return updated;
    });
  }, []);

  return {
    stocks,
    selectedStocks,
    loading,
    search,
    toggleStock,
    select,
    deselect,
  };
};

export default useStocks;
