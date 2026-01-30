import { useState } from 'react';
import { Button, Input, Card } from './common';

const Optimize = () => {
  const stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA', 'META', 'NVDA', 'JPM', 'BAC', 'WMT'];
  const [selected, setSelected] = useState([]);
  const [lambda, setLambda] = useState(0.5);

  const toggleStock = (stock) => {
    setSelected((prev) =>
      prev.includes(stock) ? prev.filter((s) => s !== stock) : [...prev, stock],
    );
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">Portfolio Optimizer</h1>
        <p className="text-gray-400">Optimize your portfolio using sentiment analysis</p>
      </div>

      <Card title="Stock Selection">
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2">
          {stocks.map((stock) => (
            <button
              key={stock}
              onClick={() => toggleStock(stock)}
              className={`py-2 px-3 rounded-lg font-semibold transition-smooth ${
                selected.includes(stock)
                  ? 'bg-accent text-primary'
                  : 'border border-accent/30 text-accent hover:border-accent'
              }`}
              type="button"
            >
              {stock}
            </button>
          ))}
        </div>
        <p className="text-gray-400 text-sm mt-4">
          Selected: {selected.length} stocks (Minimum 3 required)
        </p>
      </Card>

      <Card title="Parameters">
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-semibold mb-2">
              Sentiment Weight (λ): {lambda.toFixed(1)}
            </label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={lambda}
              onChange={(e) => setLambda(parseFloat(e.target.value))}
              className="w-full"
            />
          </div>

          <Input
            label="Risk-Free Rate (%)"
            type="number"
            placeholder="e.g., 5.0"
            defaultValue="5.0"
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input label="Start Date" type="date" />
            <Input label="End Date" type="date" />
          </div>
        </div>
      </Card>

      <Button
        disabled={selected.length < 3}
        className="w-full"
        size="lg"
      >
        Optimize Portfolio
      </Button>
    </div>
  );
};

export default Optimize;
