import { Card, StatCard, LoadingSpinner } from './common';

const Dashboard = () => {
  const stats = [
    { label: 'Annual Return', value: '+24.5%', change: '+5.2%', trend: 'positive' },
    { label: 'Sharpe Ratio', value: '1.85', change: '+0.15', trend: 'positive' },
    { label: 'Volatility', value: '12.3%', change: '-1.2%', trend: 'positive' },
    { label: 'Max Drawdown', value: '-8.5%', change: '+2.1%', trend: 'positive' },
  ];

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold mb-2">Dashboard</h1>
        <p className="text-gray-400">Welcome to your portfolio analytics hub</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <StatCard key={stat.label} {...stat} />
        ))}
      </div>

      {/* Portfolio Allocation Card */}
      <Card title="Portfolio Allocation" className="col-span-full">
        <div className="flex items-center justify-center py-12">
          <LoadingSpinner size="lg" center />
        </div>
      </Card>

      {/* Sentiment Analysis Card */}
      <Card title="Sentiment Analysis" className="col-span-full">
        <div className="space-y-4">
          <div className="bg-secondary rounded-lg p-4">
            <p className="text-sm text-gray-400 mb-2">Market Sentiment</p>
            <div className="w-full bg-secondary rounded-full h-2">
              <div className="bg-gradient-to-r from-accent to-green-400 h-2 rounded-full w-3/4 glow" />
            </div>
            <p className="text-accent text-sm mt-2">Bullish (75%)</p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default Dashboard;
