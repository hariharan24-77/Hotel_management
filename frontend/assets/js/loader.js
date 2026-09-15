const Loader = {
  element: null,

  init() {
    this.element = document.getElementById("globalLoader");
  },

  show() {
    if (!this.element) {
      this.init();
    }

    if (this.element) {
      this.element.classList.remove("d-none");
    }
  },

  hide() {
    if (!this.element) {
      this.init();
    }

    if (this.element) {
      this.element.classList.add("d-none");
    }
  },
};
