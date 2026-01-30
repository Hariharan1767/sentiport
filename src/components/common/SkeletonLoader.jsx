/**
 * SkeletonLoader - Shimmer loading placeholder
 */

import PropTypes from 'prop-types';

const SkeletonLoader = ({ lines = 3, height = 4, width = 'w-full' }) => {
  return (
    <div className="space-y-3">
      {Array.from({ length: lines }).map((_, i) => (
        <div
          key={i}
          className={`${width} bg-secondary rounded animate-pulse`}
          style={{ height: `${height * 4}px` }}
        />
      ))}
    </div>
  );
};

SkeletonLoader.propTypes = {
  lines: PropTypes.number,
  height: PropTypes.number,
  width: PropTypes.string,
};

export default SkeletonLoader;
