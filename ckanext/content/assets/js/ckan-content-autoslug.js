ckan.module('ckan-content-autoslug', function ($) {
  return {
    options: {
      prefix: '',
      target: null
    },
    initialize: function () {
      $.proxyAll(this, /_on/);
      const target = $('[name="'+ this.options.target+ '"]').first();
      const prefix = this.options.prefix ? '/' + this.options.prefix : '';
      let autofill = false;

      this.el.on('input', () => {
        autofill = false
        if (!this.el.val()) {
          autofill = true;
        }
      });

      target.on('input', () => {
        if (!this.el.val() || autofill) {
          this.el.val(prefix + '/' + this._slugify(target.val()));
        }
      });
    },
    _slugify: function (text) {
      return text
        .toLowerCase()
        .replace(/[^\w\s-]/g, '')        // Remove all non-word, non-space, non-hyphen characters
        .trim()
        .replace(/[\s_]+/g, '-')         // Replace spaces and underscores with single hyphen
        .replace(/-+/g, '-')             // Collapse multiple hyphens into one
        .replace(/^-+|-+$/g, '');        // Trim leading/trailing hyphens
    }
  };
});
