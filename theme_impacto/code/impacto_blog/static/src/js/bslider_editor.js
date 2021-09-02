odoo.define('impacto_blog.bslider_editor', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var rpc = require('web.rpc');

    var options = require('web_editor.snippets.options');
    var wUtils = require('website.utils');
    var qweb = core.qweb;
    
    
	ajax.loadXML('/impacto_blog/static/src/xml/blog_template.xml', core.qweb);
	options.registry['bslider_snippet_option_modify'] = options.Class.extend({
 
		modify: function(type,value) {
     
			var self = this;
			if(type == 'click' || type == 'reset' || type == false ){
				self.$modal = $(qweb.render("comercio_web.blog_slider_popup"));
				self.$modal.appendTo('body');
				self.$modal.modal();	
				var $collection_opt =self.$modal.find("#productcollection");
        var $collection_text = '';
				
				var $limit =self.$modal.find("#limit");
				
				var $submit = self.$modal.find("#submit");
				rpc.query({
					model: "blogcollection",
					method: "search_read",
				  args: ['', []],
				}).then(function(i) {	
					$collection_opt.find("#option").remove();
					$(i).each(function() {
						var t = $(this);
             $collection_opt.append('<option value="' + t[0].id + '">' + t[0].name + '</option>');  	
						
						var collection_id = self.$target.attr("data-collection-id");
						$collection_opt.val(collection_id);
						
                                                                        
						var slidertype= self.$target.attr("data-slider-type");
						
						var limit =  self.$target.attr("data-slider-limit");
                      
						$limit.val(limit);
						
						
                    });			
				});
				
				$submit.on('click', function() {
                      self.$target.attr("data-collection-id", $collection_opt.val());
                      
					  self.$target.attr("data-slider-limit", $limit.val());
                     self.$target.empty().append('<div class="seaction-heading"><h1>'+ $collection_opt.text() +'</h1></div>');                                                 
					 
                });
			}         
            return self;   
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