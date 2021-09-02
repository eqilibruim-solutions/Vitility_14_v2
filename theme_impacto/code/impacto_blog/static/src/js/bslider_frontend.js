odoo.define('impacto_blog.bcarousel_frontend', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var sAnimation = require('website.content.snippets.animation');
    var publicWidget = require('web.public.widget');
    
    publicWidget.registry.bslider_snippet_option = publicWidget.Widget.extend({
        selector: ".bslider_snippet_option",
        disabledInEditableMode: false,
        start: function() {
            this.redraw()
        },
        destroy: function() {
            this.clean(), this._super.apply(this, arguments)
        },
        redraw: function(t) {
            this.clean(t), this.build(t)
        },
        clean: function(t) {
            this.$target.empty()
        },
        carousel_view: function(t) {
            $(".owl-carousel").owlCarousel({
                loop: !0,
                margin: 10,
                responsiveClass: !0,
                dots: !1,
                nav: !0,
                pagination: !1,
                autoplay: !1,
                responsive: {
                    768: {
                        items: 2
                    },
                    979: {
                        items: 2
                    },
                    479: {
                        items: 1
                    },
                    320: {
                        items: 1
                    },
                    1199: {
                        items: this.$target.data("objects_in_slide")
                    }
                }
            })
        },
        build: function(t) {
				//debugger;
            var e = this,
                i = e.$target.data("slider-limit"),
                a = e.$target.data("collection-id"),
                s = e.$target.data("template"),
				n = 10;
            e.$target.attr("contentEditable", 'False'), n || (n = 3), i || (i = 3);
            ajax.jsonRpc("/blog/get_blog_content", "call", {
                template: s,
                collection_id: a,
                limit: i
            }).then(function(t) {
                $(t).appendTo(e.$target), e.carousel_view(t)
            });
        },
        loading: function(t) {}
    });
});