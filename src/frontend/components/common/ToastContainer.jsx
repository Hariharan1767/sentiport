import React from 'react';
import { Toast } from './Toast';

// ToastContainer component for displaying multiple toasts
export const ToastContainer = ({ toasts, onClose }) => {
  if (!toasts || toasts.length === 0) return null;
  
  return (
    <div className="fixed top-4 right-4 z-50 flex flex-col gap-2 max-w-sm">
      {toasts.map((toast) => (
        <Toast
          key={toast.id}
          id={toast.id}
          message={toast.message}
          type={toast.type}
          onClose={() => onClose(toast.id)}
        />
      ))}
    </div>
  );
};

export default ToastContainer;
