/**
 * Toast notification component for displaying messages
 */

import PropTypes from 'prop-types';
import { X, CheckCircle, AlertCircle, AlertTriangle, Info } from 'lucide-react';

const Toast = ({ id, message, type, onClose }) => {
  const typeStyles = {
    success: {
      bg: 'bg-green-900/30',
      border: 'border-accent',
      icon: CheckCircle,
      color: 'text-accent',
    },
    error: {
      bg: 'bg-red-900/30',
      border: 'border-danger',
      icon: AlertCircle,
      color: 'text-danger',
    },
    warning: {
      bg: 'bg-yellow-900/30',
      border: 'border-warning',
      icon: AlertTriangle,
      color: 'text-warning',
    },
    info: {
      bg: 'bg-blue-900/30',
      border: 'border-blue-400',
      icon: Info,
      color: 'text-blue-400',
    },
  };

  const style = typeStyles[type] || typeStyles.info;
  const Icon = style.icon;

  return (
    <div className={`${style.bg} border ${style.border} rounded-lg p-4 flex items-start gap-3 mb-3 max-w-md animate-slideInRight`}>
      <Icon className={`w-5 h-5 ${style.color} flex-shrink-0 mt-0.5`} />
      <div className="flex-1">
        <p className="text-white text-sm">{message}</p>
      </div>
      <button
        type="button"
        onClick={() => onClose(id)}
        className="text-gray-400 hover:text-white"
      >
        <X className="w-4 h-4" />
      </button>
    </div>
  );
};

Toast.propTypes = {
  id: PropTypes.number.isRequired,
  message: PropTypes.string.isRequired,
  type: PropTypes.oneOf(['success', 'error', 'warning', 'info']),
  onClose: PropTypes.func.isRequired,
};

/**
 * Toast Container component
 */
const ToastContainer = ({ toasts, onClose }) => {
  return (
    <div className="fixed bottom-4 right-4 z-50">
      {toasts.map((toast) => (
        <Toast key={toast.id} {...toast} onClose={onClose} />
      ))}
    </div>
  );
};

ToastContainer.propTypes = {
  toasts: PropTypes.array.isRequired,
  onClose: PropTypes.func.isRequired,
};

export { Toast, ToastContainer };
