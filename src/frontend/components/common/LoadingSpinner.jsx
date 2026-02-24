import PropTypes from 'prop-types';

const LoadingSpinner = ({ size = 'md', center = false }) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
  };

  const dotClasses = {
    sm: 'w-1.5 h-1.5',
    md: 'w-2 h-2',
    lg: 'w-3 h-3',
  };

  return (
    <div className={`flex gap-1.5 ${center ? 'items-center justify-center' : ''}`}>
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          className={`${dotClasses[size]} bg-accent rounded-full glow animate-bounce`}
          style={{
            animationDelay: `${i * 0.15}s`,
          }}
        />
      ))}
    </div>
  );
};

LoadingSpinner.propTypes = {
  size: PropTypes.oneOf(['sm', 'md', 'lg']),
  center: PropTypes.bool,
};

export default LoadingSpinner;
