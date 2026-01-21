ckan.module("ckan-content-list", function ($) {
    return {
        initialize: function () {
            $.proxyAll(this, /_/);

            this.contentData = null;
            this.searchTimeout = null;
            this.searchInput = $("#ckan-content-search");
            this.searchClear = $("#ckan-content-clear");

            this.table = new Tabulator("#ckan-content-list", {
                ajaxURL: this.sandbox.client.url('/api/action/ckan_content_list'),
                ajaxResponse: (url, params, response) => {
                    return this._prepareData(response);
                },
                columns: this._getColumns(),
                layout: "fitColumns",
                pagination: "local",
                paginationSize: 15,
                movableColumns: false,
                resizableRows: false,
                height: "100%",
                maxHeight: "100%",
                placeholder: this._("No content found"),
            });

            // Event listeners

            this.table.on("tableBuilt", () => {
                $(".ckan-content-search").show();
            });

            this.el.on("click", ".btn-delete", this._oncontentDelete);
            this.searchInput.on("keyup", this._onSearch);
            this.searchClear.on("click", this._onSearchClear);
        },

        /**
         * Prepare the data received from the backend
         *
         * @param {Object} data The data
         *
         * @returns {Array} The prepared data for tabulator
        */
        _prepareData: function (data) {
            const self = this;

            this.contentData = data.result.map(content => ({
                id: content.id,
                title: content.title,
                alias: content.alias,
                type: content.type,
                state: content.state,
                created: new Date(content.created + 'Z').toLocaleString(),
                modified: new Date(content.modified + 'Z').toLocaleString(),
                actions: "" // Filled dynamically by _formatActionCell
            }));

            // After rendering, hook the delete buttons
            setTimeout(() => {
                $("#ckan-content-grid").on("click", ".btn-delete", function () {
                    const contentId = $(this).data('id');
                    const contentType = $(this).data('type');
                    self._onDelete(contentId, contentType);
                });
            }, 100);

            return this.contentData;
        },


        /**
         * Get the columns for the table
         *
         * @returns {Array} The columns for the table
         */
        _getColumns: function () {
            return [
                { title: 'ID', field: 'id', visible: false },
                { title: this._("Title"), field: 'title', resizable: true},
                { title: this._("Alias"), field: 'alias', resizable: true},
                { title: this._("Type"), field: 'type', resizable: true},
                { title: this._("State"), field: 'state', resizable: true},
                { title: this._("Created"), field: 'created', resizable: false, maxWidth: 160 },
                { title: this._("Modified"), field: 'modified', resizable: false, maxWidth: 160 },
                {
                    title: this._("Actions"),
                    field: 'actions',
                    headerSort: false,
                    maxWidth: 160,
                    formatter: (cell, formatterParams, onRendered) => {
                        return this._formatActionCell(cell.getData());
                    },
                }
            ]
        },

        /**
         * Format the action cell
         *
         * @param {Object} rowData The row data
         *
         * @returns {String} The formatted action cell
         */
        _formatActionCell: function (rowData) {
            const readUrl = this.sandbox.client.url('/content/'+ rowData.type +'/' + rowData.id);
            const editUrl = this.sandbox.client.url('/content/' + rowData.type + '/edit/' + rowData.id);

            return `
                <div class="d-flex gap-2">
                    <a class="btn btn-outline-primary" href="${readUrl}">
                        <i class="fa fa-eye"></i>
                    </a>
                    <a class="btn btn-outline-primary" href="${editUrl}">
                        <i class="fa fa-pencil"></i>
                    </a>
                    <a class="btn btn-outline-danger btn-delete" data-id="${rowData.id}" data-type="${rowData.type}">
                        <i class="fa fa-trash"></i>
                    </a>
                </div>
            `;
        },

        /**
         * Delete a content
         *
         * @param {Event} e The event
         */
        _oncontentDelete: function (e) {
            const contentId = $(e.currentTarget).data('id');
            const contentType = $(e.currentTarget).data('type');
            const self = this;

            Swal.fire({
                text: this._("Are you sure you wish to delete this content?"),
                icon: "warning",
                showConfirmButton: true,
                showDenyButton: true,
                denyButtonColor: "#206b82",
                confirmButtonColor: "#d43f3a",
                denyButtonText: this._("Cancel"),
                confirmButtonText: this._("Delete"),
            }).then((result) => {
                if (result.isDenied) {
                    return;
                }

                this.sandbox.client.call(
                    "POST",
                    "delete_ckan_content",
                    { id: contentId, type: contentType },
                    function (_) {
                        Swal.fire("The content has been deleted", "", "success");
                        self.table.replaceData(); // Reload
                    },
                    function (_) {
                        Swal.fire("Unable to delete the content", "", "error");
                    }
                );
            });
        },

        /**
         * Search for a content
         *
         * @param {Event} e The event
         */
        _onSearch: function (e) {
            const self = this;
            const query = self.searchInput.val().toLowerCase();

            clearTimeout(this.searchTimeout);

            this.searchTimeout = setTimeout(() => {
                if (query) {
                    this.searchClear.addClass("search-active");
                    self.table.setFilter((row) => {
                        return [
                            row.title,
                            row.alias,
                            row.type,
                            row.state,
                            row.created,
                            row.modified,
                        ].some(value => value && value.toString().toLowerCase().includes(query));
                    });
                } else {
                    self._onSearchClear();
                }
            }, 300);
        },

        /**
         * Clear the search
         */
        _onSearchClear: function () {
            this.searchInput.val("");
            this.table.clearFilter();
            this.searchClear.removeClass("search-active");
        }
    };
});
