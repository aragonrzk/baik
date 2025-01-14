odoo.define('barcode_generator.preview_dialog', function(require) {
    'use strict';

    var Dialog = require('web.Dialog');
    var core = require('web.core');

    var PreviewDialog = Dialog.extend({
        template: 'barcode_generator.preview_dialog_template',
        events: {
            'click .o_preview_print': '_onPreviewPrint',
        },
        init: function(parent, options) {
            this._super(parent, options);
        },
        _onPreviewPrint: function() {
            // Logic to print or download
            window.print();
        },
    });

    core.action_registry.add('preview_report', PreviewDialog);
});
