const Search = {
  filter(data, keyword, fields) {
    if (!keyword) {
      return data;
    }

    const search = keyword.trim().toLowerCase();

    return data.filter((item) => {
      return fields.some((field) => {
        const value = item[field];

        if (value === null || value === undefined) {
          return false;
        }

        return value.toString().toLowerCase().includes(search);
      });
    });
  },

  bind(inputId, data, fields, render) {
    const input = document.getElementById(inputId);

    if (!input) {
      return;
    }

    input.addEventListener("keyup", function () {
      const result = Search.filter(data, this.value, fields);

      render(result);
    });
  },
};
