const Modal = {
  overlay: null,
  title: null,
  body: null,
  footer: null,

  init() {
    this.overlay = document.getElementById("appModal");
    this.title = document.getElementById("modalTitle");
    this.body = document.getElementById("modalBody");
    this.footer = document.getElementById("modalFooter");
  },

  open(title, content, footer = "") {
    if (!this.overlay) {
      this.init();
    }

    this.title.textContent = title;
    this.body.innerHTML = content;

    if (footer === "") {
      this.footer.innerHTML = `<button class="btn btn-secondary" onclick="Modal.close()">Close</button>`;
    } else {
      this.footer.innerHTML = footer;
    }

    this.overlay.classList.remove("d-none");
  },

  close() {
    if (!this.overlay) {
      this.init();
    }

    this.overlay.classList.add("d-none");
  },

  setBody(content) {
    this.body.innerHTML = content;
  },
};

document.addEventListener("click", function (e) {
  const overlay = document.getElementById("appModal");

  if (e.target === overlay) {
    Modal.close();
  }
});

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    Modal.close();
  }
});
