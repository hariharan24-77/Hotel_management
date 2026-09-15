const Validator = {
  required(value) {
    return (
      value !== null && value !== undefined && value.toString().trim() !== ""
    );
  },

  email(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  },

  phone(value) {
    return /^[6-9]\d{9}$/.test(value);
  },

  number(value) {
    return !isNaN(value);
  },

  positiveNumber(value) {
    return Number(value) > 0;
  },

  integer(value) {
    return Number.isInteger(Number(value));
  },

  minLength(value, length) {
    return value.trim().length >= length;
  },

  maxLength(value, length) {
    return value.trim().length <= length;
  },

  minValue(value, min) {
    return Number(value) >= min;
  },

  maxValue(value, max) {
    return Number(value) <= max;
  },

  date(value) {
    return !isNaN(Date.parse(value));
  },

  futureDate(value) {
    return new Date(value) > new Date();
  },

  pastDate(value) {
    return new Date(value) < new Date();
  },

  same(value1, value2) {
    return value1 === value2;
  },

  password(value) {
    return /^(?=.*[A-Z])(?=.*[a-z])(?=.*\d).{8,}$/.test(value);
  },

  clearError(input) {
    input.classList.remove("is-invalid");

    const error = input.parentElement.querySelector(".error-text");

    if (error) {
      error.remove();
    }
  },

  showError(input, message) {
    this.clearError(input);

    input.classList.add("is-invalid");

    const small = document.createElement("small");

    small.className = "error-text";

    small.textContent = message;

    input.parentElement.appendChild(small);
  },

  validateRequired(input, message) {
    if (!this.required(input.value)) {
      this.showError(input, message);

      return false;
    }

    this.clearError(input);

    return true;
  },
};
