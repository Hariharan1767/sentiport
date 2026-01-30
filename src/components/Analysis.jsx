import { Card } from './common';

const Analysis = () => {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">Analysis</h1>
        <p className="text-gray-400">Deep dive into your portfolio performance</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-4 border-b border-accent/20">
        {['Performance', 'Sentiment', 'Risk', 'Backtesting'].map((tab) => (
          <button
            key={tab}
            type="button"
            className="pb-4 px-2 border-b-2 border-accent text-accent font-semibold"
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Performance Chart Placeholder */}
      <Card title="Cumulative Returns">
        <div className="h-64 bg-secondary rounded-lg flex items-center justify-center">
          <p className="text-gray-400">Chart will render here</p>
        </div>
      </Card>

      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card title="Model Performance">
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-400">Sentiment Accuracy</span>
              <span className="font-mono font-bold">78.5%</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">R² Score</span>
              <span className="font-mono font-bold">0.821</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Direction Accuracy</span>
              <span className="font-mono font-bold">72.3%</span>
            </div>
          </div>
        </Card>

        <Card title="Data Quality">
          <div className="space-y-3">
            <div className="flex justify-between">
              <span className="text-gray-400">News Articles</span>
              <span className="font-mono font-bold">1,245</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Trading Days</span>
              <span className="font-mono font-bold">252</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-400">Coverage %</span>
              <span className="font-mono font-bold">98.5%</span>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
};

export default Analysis;
