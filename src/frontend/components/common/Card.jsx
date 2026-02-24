import PropTypes from 'prop-types';

const Card = ({
  children,
  title,
  icon: Icon,
  className = '',
}) => {
  return (
    <div className={`glass rounded-lg p-6 hover:glow-hover transition-smooth ${className}`}>
      {(title || Icon) && (
        <div className="flex items-center gap-3 mb-4">
          {Icon && <Icon className="w-5 h-5 text-accent" />}
          {title && <h3 className="text-lg font-semibold">{title}</h3>}
        </div>
      )}
      {children}
    </div>
  );
};

Card.propTypes = {
  children: PropTypes.node,
  title: PropTypes.string,
  icon: PropTypes.elementType,
  className: PropTypes.string,
};

export default Card;
