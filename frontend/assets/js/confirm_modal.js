const ConfirmModal = {
  overlay: null,
  title: null,
  message: null,
  button: null,
  callback: null,

  init() {
    this.overlay = document.getElementById("confirmModal");
    this.title = document.getElementById("confirmTitle");
    this.message = document.getElementById("confirmMessage");
    this.button = document.getElementById("confirmOkBtn");
  },

  open(title, message, callback) {
    if (!this.overlay) {
      this.init();
    }

    this.title.textContent = title;
    this.message.textContent = message;
    this.callback = callback;

    this.button.onclick = () => {
      if (typeof this.callback === "function") {
        this.callback();
      }

      this.close();
    };

    this.overlay.classList.remove("d-none");
  },

  close() {
    if (!this.overlay) {
      this.init();
    }

    this.overlay.classList.add("d-none");
  },
};

document.addEventListener("click", function (e) {
  const overlay = document.getElementById("confirmModal");

  if (e.target === overlay) {
    ConfirmModal.close();
  }
});

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    ConfirmModal.close();
  }
});
