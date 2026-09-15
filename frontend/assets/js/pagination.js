const Pagination = {
  data: [],
  page: 1,
  pageSize: 10,
  render: null,

  init(data, render) {
    this.data = data;
    this.page = 1;
    this.render = render;

    const size = document.getElementById("pageSize");

    if (size) {
      this.pageSize = Number(size.value);

      size.onchange = () => {
        this.pageSize = Number(size.value);
        this.page = 1;
        this.update();
      };
    }

    this.bindButtons();

    this.update();
  },

  bindButtons() {
    document.getElementById("firstPageBtn").onclick = () => {
      this.page = 1;
      this.update();
    };

    document.getElementById("prevPageBtn").onclick = () => {
      if (this.page > 1) {
        this.page--;
        this.update();
      }
    };

    document.getElementById("nextPageBtn").onclick = () => {
      if (this.page < this.totalPages()) {
        this.page++;
        this.update();
      }
    };

    document.getElementById("lastPageBtn").onclick = () => {
      this.page = this.totalPages();
      this.update();
    };
  },

  update() {
    const start = (this.page - 1) * this.pageSize;

    const end = start + this.pageSize;

    const rows = this.data.slice(start, end);

    this.render(rows);

    document.getElementById("pageStart").textContent =
      this.data.length === 0 ? 0 : start + 1;

    document.getElementById("pageEnd").textContent = Math.min(
      end,
      this.data.length,
    );

    document.getElementById("totalRecords").textContent = this.data.length;

    document.getElementById("pageNumber").textContent =
      `${this.page} / ${this.totalPages()}`;
  },

  totalPages() {
    return Math.max(1, Math.ceil(this.data.length / this.pageSize));
  },
};
