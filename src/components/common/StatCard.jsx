import PropTypes from 'prop-types';
import { TrendingUp, TrendingDown } from 'lucide-react';

const StatCard = ({
  label,
  value,
  change,
  trend = 'positive',
}) => {
  const TrendIcon = trend === 'positive' ? TrendingUp : TrendingDown;
  const trendColor = trend === 'positive' ? 'text-accent' : 'text-danger';

  return (
    <div className="glass rounded-lg p-6">
      <p className="text-gray-400 text-sm mb-2">{label}</p>
      <div className="flex items-end justify-between">
        <div>
          <h3 className="text-3xl font-bold bg-gradient-to-r from-accent to-green-400 bg-clip-text text-transparent">
            {value}
          </h3>
        </div>
        {change && (
          <div className={`flex items-center gap-1 ${trendColor}`}>
            <TrendIcon className="w-4 h-4" />
            <span className="text-sm font-semibold">{change}</span>
          </div>
        )}
      </div>
    </div>
  );
};

StatCard.propTypes = {
  label: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  change: PropTypes.string,
  trend: PropTypes.oneOf(['positive', 'negative']),
};

export default StatCard;
