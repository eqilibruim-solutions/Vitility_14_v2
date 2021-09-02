odoo.define('impacto_shop.slider_editor', function(require) {
    "use strict";

   
    
    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var options = require('web_editor.snippets.options');
    var wUtils = require('website.utils');
    var qweb = core.qweb;
     var _t = core._t;
     var website_sale_utils = require('website_sale.utils');
    var sAnimation = require('website.content.snippets.animation');
    
	ajax.loadXML('/impacto_shop/static/src/xml/product_template.xml', core.qweb);
 options.registry['slider_snippet_option_modify'] = options.Class.extend({

		modify: function(type,value) {
			var self = this;
			if(type == 'click' || type == 'reset' ){
				self.$modal = $(qweb.render("impacto_shop.product_slider_popup"));
				self.$modal.appendTo('body');
				self.$modal.modal();	
				var $collection_opt =self.$modal.find("#productcollection");
				var $slider_type = self.$modal.find("input[name='slidertype']");
				var $limit =self.$modal.find("#limit");
				var $price =self.$modal.find("#chkPrice");
				var $chkRatings =self.$modal.find("#chkRatings");
				var $chkAddtocart =self.$modal.find("#chkAddtocart");
				var $chkWishlist = self.$modal.find("#chkWishlist");
				var $chkQuickView = self.$modal.find("#chkQuickView");
				var $chkRibbon = self.$modal.find("#chkRibbon");
				var $ProductPerSlide = self.$modal.find("#ProductPerSlide");
				var $submit = self.$modal.find("#submit");
				rpc.query({
					model: "website.filter",
					method: "search_read",
					args: [
						[
							["Is_published", "=", !0],
							["collection_id.model_id", "=", "product.template"]
						],
						["name", "collection_id", "id"]
					]
				}).then(function(i) {	
					$collection_opt.find("#option").remove();
          var ProductPerSlide = self.$target.attr("data-product-per-slide");
						$ProductPerSlide.val(ProductPerSlide);
						
						var slidertype= self.$target.attr("data-slider-type");
						
						var limit =  self.$target.attr("data-slider-limit");
						$limit.val(limit);
						
						//alert(self.$target.attr("data-slider-price"));
						var price = self.$target.attr("data-slider-price");
                      
            if(slidertype) {
						   $("input[name=slidertype][value=" + slidertype + "]").attr('checked', 'checked');
            }                 
                                             
						if(price == 1)
						{
							$price.attr("checked","checked");
						}
						
						var Ratings =self.$target.attr("data-slider-rating");
						if(Ratings == 1)
						{
							$chkRatings.attr("checked","checked");
						}
						
						var AddToCart =self.$target.attr("data-slider-addtocart");
						if(AddToCart == 1)
						{
							$chkAddtocart.attr("checked","checked");
						}
						
						var wish = self.$target.attr("data-slider-wish");
						if(wish == 1)
						{
							$chkWishlist.attr("checked","checked");
						}
						
						var QuickView = self.$target.attr("data-slider-quick");
						if(QuickView == 1)
						{
							$chkQuickView.attr("checked","checked");
						}
						
						var Ribbon = self.$target.attr("data-slider-ribbon");
						if(Ribbon == 1)
						{
							$chkRibbon.attr("checked","checked");
						}
					$(i).each(function() {
						var t = $(this);
                        $collection_opt.append('<option value="' + t[0].id + '">' + t[0].name + '</option>');  	
						
						var collection_id = self.$target.attr("data-collection-id");
						$collection_opt.val(collection_id);
						
						
                    });			
				});
				
				$submit.on('click', function() {
                      self.$target.attr("data-collection-id", $collection_opt.val());
                      var val = self.$modal.find("input[name='slidertype']:checked").val();
                      self.$target.attr("data-slider-type", val);
					  self.$target.attr("data-slider-limit", $limit.val());
					  self.$target.attr("data-product-per-slide", $ProductPerSlide.val()); 
					  //alert($price.attr("checked","checked").length);
					  if($price.prop('checked') == true)
					  {
							self.$target.attr("data-slider-price",1);
					  }
					  else
					  {
					  
							self.$target.attr("data-slider-price",0);
					  }
					  if($chkRatings.prop('checked') == true)
					  {
							self.$target.attr("data-slider-rating",1);
					  }
					  else
					  {
							self.$target.attr("data-slider-rating",0);
					  } 
					  if($chkAddtocart.prop('checked') == true)
					  {
							self.$target.attr("data-slider-addtocart",1);
					  }
					  else
					  {
							self.$target.attr("data-slider-addtocart",0);
					  }
					  
					  if($chkWishlist.prop('checked') == true)
					  {
						  self.$target.attr("data-slider-wish",1);
					  }
					  else
					  {
						  self.$target.attr("data-slider-wish",0);
					  }
					  if($chkQuickView.prop('checked') == true)
					  {
						  self.$target.attr("data-slider-quick",1);
					  }
					  else
					  {
						  self.$target.attr("data-slider-quick",0);
					  }
					  
					  //alert($chkRibbon.attr("checked","checked").length);
					  if($chkRibbon.prop('checked') == true)
					  {
						  alert("hi");
						  self.$target.attr("data-slider-ribbon",1);
					  }
					  else
					  {
						  //alert("hi");
						  self.$target.attr("data-slider-ribbon",0);
					  }
                });
			}         
            return    
        },
        onBuilt: function() {
            var self = this;
             this._super();
             this.modify('click');
        },
        cleanForSave: function() {
            //this._super.apply(this, arguments), 
			this.$target.empty();
        }
    });
});