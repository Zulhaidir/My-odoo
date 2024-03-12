odoo.define('real_estate_ads.CustomAction', function(require) {
    "use strict";

    var abstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var CustomAction = abstractAction.extend({
        template: "CustomActionTemplate",
        start: function() {
            console.log("Action gituloh")
        }
    })

    core.action_registry.add("custom_client_action", CustomAction)
});