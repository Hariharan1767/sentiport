/**
 * Validation utilities for forms
 */

export const validateEmail = (email) => {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return re.test(email);
};

export const validateRequired = (value) => {
  return value && value.toString().trim() !== '';
};

export const validateNumber = (value) => {
  return !isNaN(parseFloat(value)) && isFinite(value);
};

export const validateRange = (value, min, max) => {
  const num = parseFloat(value);
  return num >= min && num <= max;
};

export const validateMinLength = (value, length) => {
  return value && value.toString().length >= length;
};

export const validateMaxLength = (value, length) => {
  return !value || value.toString().length <= length;
};

/**
 * Form validation schema helper
 */
export const createValidator = (schema) => (values) => {
  const errors = {};
  Object.keys(schema).forEach((field) => {
    const validators = schema[field];
    validators.forEach((validator) => {
      if (!validator.validate(values[field])) {
        errors[field] = validator.message;
      }
    });
  });
  return errors;
};
