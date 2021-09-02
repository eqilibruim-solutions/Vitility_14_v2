odoo.define('theme_impacto.theme_snippets_editor', function (require) {
    'use strict';

    var options = require('web_editor.snippets.options');
    var editor = require('web_editor.editor');
    var ajax = require('web.ajax');
    var core = require('web.core');
   //  var Model = require('web.Model');
    var qweb = core.qweb;
    var _t = core._t;
    var rpc = require('web.rpc');
     

    ajax.loadXML('/theme_impacto/static/src/xml/html_block.xml', qweb);

     options.registry.js_embed_html = options.Class.extend({
        start : function () {
			      var self = this;
			      this.id = this.$target.attr("id");
			
		    },
        edit_html: function(type,value) {
     
          var self = this;
          this.id = this.$target.attr("id");
		  /*if(type !== "click") return;*/
         if (type == "click" || type === false){
            self.$modal = $(qweb.render("theme_impacto.edit_html_modal"));
            $('body > #custom_html_modal').remove();
			      self.$modal.appendTo('body');
            self.$modal.modal();
            var $htmlvalue = self.$modal.find("#html_data"),
                $sub_data = self.$modal.find("#sub_data"); 
                $htmlvalue.val(self.$target.html());
                $sub_data.on('click', function() {
                  var html = $htmlvalue.val();
                  var live_str = $('<div>',{html:html});
                  var data = live_str.find('[data-html]');
                  var final = live_str;
                  if(data.length > 0){
                     var style = data.attr('style');
                     if(style)  self.$target.attr('style',style)
                      var cls = data.attr('class');
                      if(cls) self.$target.addClass(cls).attr('style',style);
                     var final = data.removeAttr('data-html').removeAttr('class').removeAttr('style');
                  } else {
                    
                  }
                  self.$target.empty().append(final);

        				  var oe_model = self.$target.parent().attr('data-oe-model');
        				  if(oe_model){
					          self.$target.parent().addClass('o_editable o_dirty');
				            }
                  var bar = live_str.find('.progress-bar');
                  if(bar.length > 0) IMPACTO.progressBar();

                  var counter = live_str.find('.counter');
                  if(counter.length > 0) IMPACTO.counters();

                  

                });              
             }
			      return self;
        },
        onBuilt: function() {
      			var self = this;
      			this._super();
      			this.edit_html('click');
        }
    });

    
});



