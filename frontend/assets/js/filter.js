const Filter = {
  equals(data, field, value) {
    if (value === undefined || value === null || value === "") {
      return data;
    }

    return data.filter((item) => item[field] == value);
  },

  contains(data, field, value) {
    if (value === undefined || value === null || value === "") {
      return data;
    }

    const keyword = value.toString().toLowerCase();

    return data.filter((item) => {
      const current = item[field];

      if (current === undefined || current === null) {
        return false;
      }

      return current.toString().toLowerCase().includes(keyword);
    });
  },

  dateRange(data, field, start, end) {
    return data.filter((item) => {
      const current = new Date(item[field]);

      if (start && current < new Date(start)) {
        return false;
      }

      if (end && current > new Date(end)) {
        return false;
      }

      return true;
    });
  },

  priceRange(data, field, min, max) {
    return data.filter((item) => {
      const value = Number(item[field]);

      if (min !== "" && value < Number(min)) {
        return false;
      }

      if (max !== "" && value > Number(max)) {
        return false;
      }

      return true;
    });
  },

  multiple(data, filters) {
    let result = [...data];

    filters.forEach((filter) => {
      switch (filter.type) {
        case "equals":
          result = this.equals(result, filter.field, filter.value);
          break;

        case "contains":
          result = this.contains(result, filter.field, filter.value);
          break;

        case "date":
          result = this.dateRange(
            result,
            filter.field,
            filter.start,
            filter.end,
          );
          break;

        case "price":
          result = this.priceRange(
            result,
            filter.field,
            filter.min,
            filter.max,
          );
          break;
      }
    });

    return result;
  },
};
