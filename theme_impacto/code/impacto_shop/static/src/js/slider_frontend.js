odoo.define('impacto_shop.carousel_frontend', function(require) {
    "use strict";
    
       var ajax = require('web.ajax');
    var sAnimation = require('website.content.snippets.animation');
    var core = require('web.core');
    var wUtils = require('website.utils');
    var publicWidget = require('web.public.widget');
    
     publicWidget.registry.slider_snippet_option = publicWidget.Widget.extend({
        selector: ".slider_snippet_option",
        disabledInEditableMode: false,
        start: function() {
            this.redraw();
            
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
            $(".ad_products_slider .product-slider").owlCarousel({
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
            var e = this,
                i = e.$target.data("slider-limit"),
                a = e.$target.data("collection-id"),
                n = e.$target.data("objects_in_slide"),
                s = e.$target.data("template");
            e.$target.attr("contentEditable", !1), n || (n = 3), i || (i = 6);
            ajax.jsonRpc("/slider/get_data", "call", {
                template: s,
                collection_id: a,
                objects_in_slide: n,
                slidertype: '',
                limit: i
            }).then(function(t) {
                $(t).appendTo(e.$target);
                
            var tp = e.$target.data("slider-type");

            var sl = false; /* Slider true or false */
            var fw = true; /* Full Width */
            var pd = true; /* Product padding */
            var sp = false; /* Split slide */
            var pn = 5; /* np of product */

        e.$target.removeClass('product1 product2 product3 product4 product5');
        if(tp == "style-2" || tp == "style-3"){
            sp = true;
            pn = 3; 
        } else if(tp == "style-4"){
            sl = true;
        } else if(tp == "style-5"){
            sl = true;
            fw = false;
            pn = 4; 
        } else if(tp == "style-6"){
            fw = false;
            pn = 4; 
        } else if(tp == "style-7"){
            pd = false;
            pn = 4; 
            e.$target.addClass('product-style-2');
        }

        if(fw == false) e.$target.addClass('container');
        if(sl){ 
          e.$target.find('.product-slider').addClass('owl-carousel');          	
          e.carousel_view(t);
          e.$target.removeClass('without-slider');  
        }  else{ 
          e.$target.find('.product-slider').removeClass('owl-carousel');
          e.$target.addClass('without-slider');  
        }
        
        if (sp) { 
            if (tp == "style-2") {
               // e.$target.append('<div class="imgblock" data-sticky_column><img class="img-responsive" src="/comercio_web/static/src/img/special/woman-img.jpg" alt="" /></div>');
                //e.$target.addClass('split-slider');
                //$(".split-slider .imgblock").stick_in_parent();
            } else {
                //e.$target.append('<div class="imgblock left-block" data-sticky_column><img class="img-responsive" src="/comercio_web/static/src/img/special/man-img.jpg" alt="" /></div>');
                //e.$target.addClass('split-slider split-right');
                //$(".split-slider .imgblock").stick_in_parent();
            }
        }
        else
        {
            e.$target.removeClass('split-slider split-right');
            e.$target.removeClass('split-slider');
        }
        if (pn != 5){
            e.$target.addClass('product' + pn);
        }
        else {
            e.$target.addClass('product5');
        }
            }).then(function() {
                e.loading(t)
            });
        },
        loading: function(t) {}
    });
});