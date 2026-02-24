import PropTypes from 'prop-types';

/**
 * SentimentGauge - Radial gauge visualization for sentiment score
 */
const SentimentGauge = ({ value = 0.65, min = 0, max = 1 }) => {
  const percentage = ((value - min) / (max - min)) * 100;
  const rotationDegrees = (percentage / 100) * 180 - 90;

  const getColor = () => {
    if (percentage < 33) return '#FF3860';
    if (percentage < 66) return '#FFB800';
    return '#00FF88';
  };

  const getSentiment = () => {
    if (percentage < 33) return 'Bearish';
    if (percentage < 66) return 'Neutral';
    return 'Bullish';
  };

  return (
    <div className="flex flex-col items-center justify-center py-8">
      <div className="relative w-40 h-20 mb-4">
        <div className="absolute inset-0 bg-gradient-to-r from-danger via-warning to-accent rounded-full opacity-20" />
        <div className="absolute inset-2 bg-secondary rounded-full flex items-center justify-center">
          <div
            className="absolute w-1 bg-accent rounded-full"
            style={{
              height: '60px',
              transform: `rotate(${rotationDegrees}deg)`,
              transformOrigin: 'center bottom',
              bottom: '0',
              backgroundColor: getColor(),
              boxShadow: `0 0 10px ${getColor()}`,
            }}
          />
        </div>
      </div>
      <div className="text-center">
        <p className="text-gray-400 text-sm mb-1">Market Sentiment</p>
        <h3 className="text-2xl font-bold" style={{ color: getColor() }}>
          {getSentiment()}
        </h3>
        <p className="text-accent text-xs font-mono mt-1">{(percentage / 100).toFixed(2)}</p>
      </div>
    </div>
  );
};

SentimentGauge.propTypes = {
  value: PropTypes.number,
  min: PropTypes.number,
  max: PropTypes.number,
};

export default SentimentGauge;
