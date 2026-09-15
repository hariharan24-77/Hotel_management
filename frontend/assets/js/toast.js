const Toast = {
  container: null,

  init() {
    this.container = document.getElementById("toastContainer");
  },

  show(message, type = "success", duration = 3000) {
    if (!this.container) {
      this.init();
    }

    const toast = document.createElement("div");

    toast.className = `toast toast-${type}`;

    toast.innerHTML = `
<span>${message}</span>
<button>&times;</button>
`;

    toast.querySelector("button").onclick = () => {
      this.remove(toast);
    };

    this.container.appendChild(toast);

    setTimeout(() => {
      this.remove(toast);
    }, duration);
  },

  remove(toast) {
    if (!toast) return;

    toast.classList.add("toast-hide");

    setTimeout(() => {
      toast.remove();
    }, 250);
  },

  success(message) {
    this.show(message, "success");
  },

  error(message) {
    this.show(message, "error");
  },

  warning(message) {
    this.show(message, "warning");
  },

  info(message) {
    this.show(message, "info");
  },
};
