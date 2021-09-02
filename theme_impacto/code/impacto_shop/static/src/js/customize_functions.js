odoo.define('impacto_shop.cart', function (require) {
'use strict';

var sAnimations = require('website.content.snippets.animation');
var core = require('web.core');
var _t = core._t;

var timeout;
sAnimations.registry.SaleCartLink = sAnimations.Class.extend({
    selector: '.header-icons a[href$="/shop/cart"]',
    read_events: {
        'mouseenter': '_onMouseEnter',
        'mouseleave': '_onMouseLeave',
    },

    /**
     * @override
     */
    start: function () {
        var def = this._super.apply(this, arguments);
        if (this.editableMode) {
            return def;
        }

        this.$el.popover({
            trigger: 'manual',
            animation: true,
            html: true,
            title: function () {
                return _t("My Cart");
            },
            container: 'body',
            placement: 'auto',
            template: '<div class="popover mycart-popover" role="tooltip"><div class="arrow"></div><h3 class="popover-header"></h3><div class="popover-body"></div></div>'
        });
        return def;
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     * @param {Event} ev
     */
    _onMouseEnter: function (ev) {
        var self = this;
        clearTimeout(timeout);
        $(this.selector).not(ev.currentTarget).popover('hide');
        timeout = setTimeout(function () {
            if (!self.$el.is(':hover') || $('.mycart-popover:visible').length) {
                return;
            }
            $.get("/shop/cart", {
                type: 'popover',
            }).then(function (data) {
                self.$el.data("bs.popover").config.content = data;
                self.$el.popover("show");
                $('.popover').on('mouseleave', function () {
                    self.$el.trigger('mouseleave');
                });
            });
        }, 100);
    },
    /**
     * @private
     * @param {Event} ev
     */
    _onMouseLeave: function (ev) {
        var self = this;
        setTimeout(function () {
            if ($('.popover:hover').length) {
                return;
            }
            if (!self.$el.is(':hover')) {
               self.$el.popover('hide');
            }
        }, 1000);
    },
});
});