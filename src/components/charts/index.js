import PropTypes from 'prop-types';

/**
 * CorrelationHeatmap - Display stock correlation matrix
 */
const CorrelationHeatmap = ({ correlations = {} }) => {
  const stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA'];

  const getColor = (value) => {
    if (value > 0.7) return '#00FF88';
    if (value > 0.4) return '#FFB800';
    if (value < -0.4) return '#FF3860';
    return '#1A1F3A';
  };

  const mockCorrelations = {
    'AAPL-GOOGL': 0.72,
    'AAPL-MSFT': 0.65,
    'AAPL-AMZN': 0.58,
    'AAPL-TSLA': 0.45,
    'GOOGL-MSFT': 0.68,
    'GOOGL-AMZN': 0.62,
    'GOOGL-TSLA': 0.35,
    'MSFT-AMZN': 0.61,
    'MSFT-TSLA': 0.32,
    'AMZN-TSLA': 0.28,
  };

  return (
    <div className="w-full overflow-x-auto">
      <div className="inline-block min-w-full">
        {/* Header */}
        <div className="flex gap-1">
          <div className="w-20" />
          {stocks.map((stock) => (
            <div
              key={stock}
              className="w-20 text-center text-sm font-semibold text-accent"
            >
              {stock}
            </div>
          ))}
        </div>

        {/* Heatmap rows */}
        {stocks.map((stock1, i) => (
          <div key={stock1} className="flex gap-1 mb-1">
            <div className="w-20 text-sm font-semibold text-accent flex items-center">
              {stock1}
            </div>
            {stocks.map((stock2, j) => {
              const key = i <= j ? `${stock1}-${stock2}` : `${stock2}-${stock1}`;
              const value = mockCorrelations[key] || (i === j ? 1 : 0.5);
              return (
                <div
                  key={`${stock1}-${stock2}`}
                  className="w-20 h-10 flex items-center justify-center text-xs font-mono font-bold rounded transition-all hover:shadow-glow"
                  style={{
                    backgroundColor: getColor(value),
                    color: '#0A0E27',
                  }}
                  title={`${stock1}-${stock2}: ${value.toFixed(2)}`}
                >
                  {value.toFixed(2)}
                </div>
              );
            })}
          </div>
        ))}

        {/* Legend */}
        <div className="mt-4 flex gap-4 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded" style={{ backgroundColor: '#FF3860' }} />
            <span>Negative</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded" style={{ backgroundColor: '#FFB800' }} />
            <span>Neutral</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded" style={{ backgroundColor: '#00FF88' }} />
            <span>Positive</span>
          </div>
        </div>
      </div>
    </div>
  );
};

CorrelationHeatmap.propTypes = {
  correlations: PropTypes.object,
};

export default CorrelationHeatmap;
